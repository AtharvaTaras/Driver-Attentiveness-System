# Driver-Attentiveness-System
A Python program that checks driver attentiveness using computer vision.  
Work In Progress  
*Project Submission for AICTE Eduskills IBM Internship (Dec 2022 - Jan 2023)*  

### Prerequisites  
- Python 3.8.5
- Visual C++
- OpenCV
- Numpy
- OS
- DateTime
- Dlib
- Face-Detector
- Cmake
___

To create a custom Python virtual environment   
```commandline
python -m venv custom_venv
```  
```commandline
custom_venv\Scripts\activate.bat  
``` 

Install all requirements at once  
```commandline
pip intall -r requirements.txt
```
---
You may run into errors while installing dlib, try this to fix it (worked for me)  

1. Make sure you have the latest version of [Microsoft Visual C++](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) installed  

2. Clone [this repository](https://github.com/datamagic2020/Install-dlib) to get all the wheel (.wh) files
```commandline
git clone https://github.com/datamagic2020/Install-dlib.git
```
3. Install using manually specifying file path
```commandline
pip install "path_to_cloned_repo\wheel_package_for_your_python_version"
```
4. You can check your installed Python version using
```commandline
python -V
```