#include <iostream>
#include <fstream>
#include <vector>
#include <opencv2/opencv.hpp>

struct Fragment {
    int index;
    int posX;
    int posY;
    double angle;
};

int main() {

    // Load original image
    cv::Mat fresque = cv::imread("./assets/fresque.jpg", cv::IMREAD_UNCHANGED);


    // Create fragments list from fragments.txt
    std::vector<Fragment> fragments;
    std::ifstream fragmentsFile("./assets/fragments.txt");
    if (fragmentsFile.is_open()) {
        Fragment fragment;
        // On each iteration extract data to fragment struct
        while (fragmentsFile >> fragment.index >> fragment.posX >> fragment.posY >> fragment.angle) {
            fragments.push_back(fragment);
        }
        fragmentsFile.close();
    } else {
        std::cout << "Error while opening fragments.txt" << std::endl;
        return -1;
    }
    /*for (const auto &fragment: fragments) {
        // Load fragment
        std::string fragmentFileName = "./assets/frag_eroded/frag_eroded_" + std::to_string(fragment.index) + ".png";
        cv::Mat frag = cv::imread(fragmentFileName, cv::IMREAD_ANYDEPTH);
        if (frag.empty()) {
            std::cout << "Error while loading fragment " << fragmentFileName << std::endl;
            continue;
        }

        cv::Mat insetImage(fresque, cv::Rect(fragment.posX, fragment.posY, frag.cols, frag.rows));
        frag.copyTo(insetImage);

    }*/

    cv::Mat frag = cv::imread("./assets/frag_eroded/frag_eroded_0.png", cv::IMREAD_UNCHANGED);

    cv::Mat alpha(frag.rows, frag.cols, CV_8UC1);
    cv::extractChannel(frag, alpha, 3);

    cv::multiply(alpha, frag, frag);
    cv::multiply(1.0-alpha, fresque, fresque);

    cv::Mat result;
    cv::add(frag, fresque, result);

    cv::imshow("result", result);
    cv::waitKey(0);

    return 0;
}
