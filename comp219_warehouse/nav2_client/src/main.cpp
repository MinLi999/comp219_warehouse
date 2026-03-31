#include "nav2_client/navigation_client.hpp"
#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <string>
#include <vector>

void displayMenu() {
    std::cout << "\n===========================================" << std::endl;
    std::cout << "   IT Warehouse Task Management System" << std::endl;
    std::cout << "===========================================" << std::endl;
    std::cout << "Select Item Category:" << std::endl;
    std::cout << "1. PCs & Monitors (Room 1)" << std::endl;
    std::cout << "2. Laptops (Room 2)" << std::endl;
    std::cout << "3. Accessories (Room 3)" << std::endl;
    std::cout << "4. Cables (Room 4)" << std::endl;
    std::cout << "0. Exit System" << std::endl;
    std::cout << "Choice [0-4]: ";
}

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NavigationClient>();

    RCLCPP_INFO(node->get_logger(), "=== IT Warehouse System Start ===");
    // Automatically perform the "2D Pose Estimate" action
    node->setInitialPose();

    while (rclcpp::ok()) {
        displayMenu();
        
        int item_choice;
        if (!(std::cin >> item_choice)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }

        if (item_choice == 0) break;

        std::string item_type;
        switch (item_choice) {
            case 1: item_type = "pc"; break;
            case 2: item_type = "laptop"; break;
            case 3: item_type = "accessory"; break;
            case 4: item_type = "cable"; break;
            default:
                std::cout << "Invalid choice, please try again." << std::endl;
                continue;
        }

        std::cout << "\nSelect Task Direction:" << std::endl;
        std::cout << "1. Inbound (Service Desk -> Storage Room)" << std::endl;
        std::cout << "2. Outbound (Storage Room -> Service Desk)" << std::endl;
        std::cout << "Choice [1-2]: ";

        int task_choice;
        std::cin >> task_choice;
        bool is_inbound = (task_choice == 1);

        RCLCPP_INFO(node->get_logger(), "Starting mission for %s...", item_type.c_str());

        // 调用你已经在 navigation_client.cpp 中写好的逻辑
        if (node->manageWarehouseTask(item_type, is_inbound)) {
            RCLCPP_INFO(node->get_logger(), "Mission completed successfully!");
        } else {
            RCLCPP_ERROR(node->get_logger(), "Mission failed.");
        }
    }

    RCLCPP_INFO(node->get_logger(), "Shutting down IT Warehouse System.");
    rclcpp::shutdown();
    return 0;
}