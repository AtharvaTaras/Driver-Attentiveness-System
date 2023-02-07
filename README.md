# Driver-Attentiveness-System

**Project Submission for IBM Internship (AICTE, Edunet Foundation Dec 2022 - Feb 2023 Batch)**  
[Atharva Taras](https://www.linkedin.com/in/atharvataras/) (AI_ADV_21 Dec)  
AISSMS Institute of Information Technology, Pune

A Python program that checks driver attentiveness using computer vision.  
[View Presentation](https://github.com/AtharvaTaras/Driver-Attentiveness-System/tree/master/presentation)  
[View Source Code](https://github.com/AtharvaTaras/Driver-Attentiveness-System/blob/master/main_v2.py)  

<pre>
<h3>Prerequisites</h3>
> Python 3.8.5
> Visual C++
> OpenCV
> Numpy
> OS
> DateTime
> Dlib
> Face-Recognition
> Cmake
> SciPy
> Time
> Imutils
> Winsound
> Pushbullet (API and Mobile App)
> Socket

</pre>

Sample Outputs -    

https://user-images.githubusercontent.com/78966432/214768519-b1be7019-18cf-44cd-b635-0d4d334e1a4b.mp4

https://user-images.githubusercontent.com/78966432/214768609-7b2e8e61-93a0-4d0e-b992-7c650d63fd68.mp4

https://user-images.githubusercontent.com/78966432/214768627-a8e3c380-e65d-4664-8021-e13a23b69900.mp4

https://user-images.githubusercontent.com/78966432/214768661-8b7b809a-f372-4ad4-8fae-d1728618fe14.mp4

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

2. Clone [this repository](https://github.com/datamagic2020/Install-dlib) to get all the wheel (.whl) files
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
---





