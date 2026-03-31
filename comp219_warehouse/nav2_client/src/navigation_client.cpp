#include "nav2_client/navigation_client.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
#include <chrono>
#include <thread>

NavigationClient::NavigationClient() : Node("navigation_client"),
    goal_accepted_(false),
    navigation_complete_(false),
    navigation_successful_(false)
{
    action_client_ = rclcpp_action::create_client<NavigateToPose>(
        this, "navigate_to_pose");
        
    locations_["initial_pose"] = {-0.04, -0.06, 0.0};
    locations_["it_service_desk"] = {0.388, -22.3, 0.0};
    locations_["room1"] = {4.77, -4.11, 0.0};    // PCs & Monitors        
    locations_["room2"] = {7.45, -10.5, 0.0};    // Laptops      
    locations_["room3"] = {-0.549, -11, 0.0};    // Accessories      
    locations_["room4"] = {0.848, -15.4, 0.0};   // Cables       
    
    RCLCPP_INFO(get_logger(), "Centennial IT Warehouse Navigation client initialized");

    auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(1)).transient_local();
    initial_pose_pub_ = this->create_publisher<geometry_msgs::msg::PoseWithCovarianceStamped>("/initialpose", qos_profile);
    RCLCPP_INFO(get_logger(), "Navigation client with Auto-Initial-Pose initialized");
}

// 2. Get the intial position of the robot in the map
bool NavigationClient::setInitialPose()
{
    RCLCPP_INFO(get_logger(), "Waiting for AMCL to subscribe to /initialpose...");
    while (initial_pose_pub_->get_subscription_count() == 0 && rclcpp::ok()) {
        // Keep spinning to allow the publisher to establish connection with AMCL's subscriber
        rclcpp::spin_some(this->get_node_base_interface());
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    auto msg = geometry_msgs::msg::PoseWithCovarianceStamped();
    msg.header.frame_id = "map";
    msg.header.stamp = this->now();

    // use map_locations.yaml's initial_pose as the robot's starting point
    auto init = locations_["initial_pose"];
    msg.pose.pose.position.x = init.x; // -0.04
    msg.pose.pose.position.y = init.y; // -0.06
    msg.pose.pose.orientation.w = 1.0;  // default orientation (facing forward)

    // Simulate the covariance matrix of 2D Pose Estimation
    msg.pose.covariance[0] = 0.25;
    msg.pose.covariance[7] = 0.25;
    msg.pose.covariance[35] = 0.06;

    RCLCPP_INFO(get_logger(), "Setting initial pose automatically...");
    initial_pose_pub_->publish(msg);
    
    // Give the system some time to clear the cost map
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return true;
}


bool NavigationClient::navigate2Pose(double x, double y, double z, double orientation_w)
{
    navigation_complete_ = false;
    navigation_successful_ = false;
    goal_accepted_ = false;

    while (!action_client_->wait_for_action_server(std::chrono::seconds(1))) {
        RCLCPP_INFO(get_logger(), "Waiting for action server...");
    }

    auto goal_msg = NavigateToPose::Goal();
    goal_msg.pose.header.frame_id = "map";
    goal_msg.pose.header.stamp = this->now();
    
    goal_msg.pose.pose.position.x = x;
    goal_msg.pose.pose.position.y = y;
    goal_msg.pose.pose.position.z = z;
    
    goal_msg.pose.pose.orientation.w = orientation_w;
    goal_msg.pose.pose.orientation.x = 0.0;
    goal_msg.pose.pose.orientation.y = 0.0;
    goal_msg.pose.pose.orientation.z = 0.0;

    RCLCPP_INFO(get_logger(), "Navigating to position: x=%.2f, y=%.2f, z=%.2f", x, y, z);
    
    auto send_goal_options = rclcpp_action::Client<NavigateToPose>::SendGoalOptions();
    send_goal_options.goal_response_callback =
        std::bind(&NavigationClient::goalResponseCallback, this, std::placeholders::_1);
    send_goal_options.feedback_callback =
        std::bind(&NavigationClient::feedbackCallback, this, std::placeholders::_1, std::placeholders::_2);
    send_goal_options.result_callback =
        std::bind(&NavigationClient::resultCallback, this, std::placeholders::_1);

    auto goal_future = action_client_->async_send_goal(goal_msg, send_goal_options);
    
    if (rclcpp::spin_until_future_complete(shared_from_this(), goal_future) != 
        rclcpp::FutureReturnCode::SUCCESS)
    {
        RCLCPP_ERROR(get_logger(), "Failed to send goal");
        return false;
    }

    // Wait for goal to complete
    while (!navigation_complete_ && rclcpp::ok()) {
        rclcpp::spin_some(shared_from_this());
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    if (!navigation_successful_) {
        RCLCPP_ERROR(get_logger(), "Navigation failed");
        return false;
    }

    // Add delay between consecutive goals
    std::this_thread::sleep_for(std::chrono::seconds(2));
    
    return true;
}

/**
 * @param item_type: "pc", "laptop", "accessory", "cable"
 * @param is_inbound: true means storing staff into room (Desk -> Room), false means retrieving staff from room (Room -> Desk)
 */
bool NavigationClient::manageWarehouseTask(std::string item_type, bool is_inbound)
{
    // 1. make sure item type is valid and get target room
    std::string target_room;
    if (item_type == "pc") target_room = "room1";
    else if (item_type == "laptop") target_room = "room2";
    else if (item_type == "accessory") target_room = "room3";
    else if (item_type == "cable") target_room = "room4";
    else {
        RCLCPP_ERROR(get_logger(), "Unknown item type!");
        return false;
    }

    auto desk = locations_["it_service_desk"];
    auto room = locations_[target_room];
    auto home = locations_["initial_pose"];

    if (is_inbound) {
        // --- Storage logic: Service Desk -> Room ---
        RCLCPP_INFO(get_logger(), "INBOUND: Collecting %s from Service Desk...", item_type.c_str());
        if (!navigate2Pose(desk.x, desk.y, desk.z)) return false;
        std::this_thread::sleep_for(std::chrono::seconds(5)); // Loading

        RCLCPP_INFO(get_logger(), "Storing %s in %s...", item_type.c_str(), target_room.c_str());
        if (!navigate2Pose(room.x, room.y, room.z)) return false;
    } 
    else {
        // --- Outbound logic: Room -> Front Desk ---
        RCLCPP_INFO(get_logger(), "OUTBOUND: Fetching %s from %s...", item_type.c_str(), target_room.c_str());
        if (!navigate2Pose(room.x, room.y, room.z)) return false;
        std::this_thread::sleep_for(std::chrono::seconds(5)); // Fetching

        RCLCPP_INFO(get_logger(), "Delivering %s to Service Desk...", item_type.c_str());
        if (!navigate2Pose(desk.x, desk.y, desk.z)) return false;
    }

    // Return to standby point after task completion
    RCLCPP_INFO(get_logger(), "Mission complete. Returning home...");
    return navigate2Pose(home.x, home.y, home.z);
}

void NavigationClient::goalResponseCallback(
    std::shared_ptr<GoalHandleNavigateToPose> goal_handle)
{
    if (!goal_handle) {
        goal_accepted_ = false;
        RCLCPP_ERROR(get_logger(), "Goal was rejected by server");
    } else {
        goal_accepted_ = true;
        RCLCPP_INFO(get_logger(), "Goal accepted by server");
    }
}

void NavigationClient::feedbackCallback(
    GoalHandleNavigateToPose::SharedPtr goal_handle,
    const std::shared_ptr<const NavigateToPose::Feedback> feedback)
{
    (void)goal_handle;  // Unused
    double distance_remaining = feedback->distance_remaining;
    RCLCPP_INFO(get_logger(), "Distance remaining: %.2f", distance_remaining);
}

void NavigationClient::resultCallback(
    const GoalHandleNavigateToPose::WrappedResult & result)
{
    navigation_complete_ = true;
    switch (result.code) {
        case rclcpp_action::ResultCode::SUCCEEDED:
            navigation_successful_ = true;
            RCLCPP_INFO(get_logger(), "Navigation successful");
            break;
        case rclcpp_action::ResultCode::ABORTED:
            navigation_successful_ = false;
            RCLCPP_ERROR(get_logger(), "Navigation aborted");
            break;
        case rclcpp_action::ResultCode::CANCELED:
            navigation_successful_ = false;
            RCLCPP_ERROR(get_logger(), "Navigation canceled");
            break;
        default:
            navigation_successful_ = false;
            RCLCPP_ERROR(get_logger(), "Unknown result code");
            break;
    }
}
