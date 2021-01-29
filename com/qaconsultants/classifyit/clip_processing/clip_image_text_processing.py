import csv

import torch
import pandas as pd
from PIL import Image
from numpy import loadtxt

from com.qaconsultants.classifyit.clip_processing import clip


def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start + n]


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# categories_list = list(chunks(
#     "QA Consultants’ Team and Management Comprehensive Solution Delivery Proof of Concepts and Pilots SDLC (Software Development Life Cycle) Tool Optimization Staff Augmentation Training and Knowledge Transfer Knight Capital, a trading firm in New Jersey City, lost $10 million dollars a minute in 2012 largely in part because they didn’t test their automated trading software. Let that sink in. By the time someone caught the error, the company had lost $440 million, which is more than the company’s revenue of $289 million (in the second quarter). Though this example is an anomaly in terms of extravagant losses, it’s a painful one to realize. This could have easily been avoided if the software development process had included a quality assurance test automation expert that evaluated the software testing approach. The testing process in itself will save money, headaches, and reputation loss; it’s worth the investment. Clients Training and Knowledge Transfer Micro Focus Selenium Cucumber Mobile Labs Sonar QA Consultants is recognized for our broad and expansive test automation capabilities, architecture, building, and maintaining test automation solutions. In turn, we support multi-platform, multi-device, and multi-language/OS forms. QA Consultants applies high levels of sophisticated test automation, utilizing risk-based methodologies, and builds for our clients. We use comprehensive testing modules and libraries for improved productivity including speed to execution. Our model delivers on the promise of a significantly higher quality of testing time to value. In the past four years, over 80% of test projects we’ve completed the required automation. As a result, test automation has driven testing costs down and drastically improve the reusability of automation scripts. With this strength comes innovation in automation in our Test Factory™ that dictates best practices and processes. Micro Focus Worksoft Open Source Tools The earlier automation of manual testing artefacts (Shift-Left) BMO Case Study: Test Automation, Functional Testing CHALLENGE & TEST REQUIREMENTS Our test automation engineering solution components: BMO The right tools: Pytes Read more about our Services iVinci Health Treatment Case Study: Manual and Automated Testing “QA Consultants provided a Analytics 4 Life Case Study: Test Automation (API), Functional, Performance, and Security testing The non-technical stream denotes that the QA Testers are more manual based testers. As such, they are capable to interface with test automation via certain front ends that have been provided to them. These front ends include a keyword, gherkin, etc. IBM The right people: Fakery SDLC (Software Development Life Cycle) Tool Optimization Case Study: Test Automation, Functional Testing CHALLENGE & TEST REQUIREMENTS Test Talk Case Study: Test Automation (API), Functional, Performance, and Security testing Tricentis Python Pytes Appium Fakery What happens when test automation goes wrong? Appium Deliver projects faster The right process: Selenium Although for agile things are slightly different from waterfall. Within agile, the test automation can begin from the start of the phase to phase process. However, even then test automation’s test coverage will be behind. Nonetheless, test automation itself is creating the regressions test set. test automation The usage of open source automation solutions as viable alternatives to commercial tools QA Consultants is tools agnostic. We provide solutions based on our clients’ needs. QA Consultants can readily customize any solution. From the high-level conceptual design down to the exact toolset that makes sense to deploy. Staff Augmentation Our Testing Services Decrease budgets DeviceAnywhere QA Consultants is at the forefront of test automation engineering techniques, technologies, and methodologies with our test automation services. We partner with clients across various industries to drive their automation innovation and QA optimization. Our expertise spans all test automation platforms and we have a vast knowledge base of best practices which we leverage for our clients. QA Consultants deploys a “Test Automation Solution” approach to execute best practice QA processes. By working in a collaborative team environment we’re able to produce quality and expedient results. The seasoned expertise of QA Consultants’ test teams becomes more significant when training, orientation, and familiarity with the environment becomes a factor. Our responsiveness to our clients’ needs will ensure a quality outcome, deep rigor, and the use of comprehensive test governance. From an efficiency and effectiveness manner, we have the required knowledge and confidence in our ability to execute project deliverables. Clients will benefit from a quick ramp up, agile project delivery, and a high productivity team. The reduction in manual testing time and effort for regression testing Commercial Tools There are two types of popular test automation tools in the market place, those being open source and commercial. The open-source tools revolve around selenium and different languages that can be used with selenium. Languages such as java, javascript, c-sharp, C++, python, groovy, and others. Katalon is a tool based on Selenium and is the natural evolution of open source tools. Commercial tools revolve around Micro Focus, Tricentis, Parasoft, IBM Rational, and Worksoft Certify. Worksoft Katalon WebDriver IO ZAPTEST A sample of our platforms, tools, and technologies include: Commercial Tools Open Source Tools Customizable Frameworks Mobile Device Management & Automation Other Solution Components JavaScript Mobile Device Management & Automation Sonar Here’s what we have to say about Test Automation and being tool agnostic. Analytics 4 Life Contact Us Test Automation Today Regular and rapid regression testing The earlier automation of manual testing artefacts (Shift-Left) The utilization of continuous testing (CI/CD) The automation of both unit testing and API testing Natural language test design (i.e. Gherkin via TDD, BDD) that facilitates ease and quicker automated test scripting The reduction in manual testing time and effort for regression testing The usage of open source automation solutions as viable alternatives to commercial tools iVinci Health Treatment Mobile Labs team The utilization of continuous testing (CI/CD) Jenkins The technical stream indicates that the QA Testers have a development background. Meaning they can get into creating test frameworks and essentially the guts of the test automation. When doing so they may be working in languages such as Java, C++, etc. BMO Case Study: Test Automation, Functional Testing CHALLENGE & TEST REQUIREMENTS iVinci Health Treatment Case Study: Manual and Automated Testing “QA Consultants provided a Paradigm Quest Case Study #1: Test Automation (Jira/Zephyr Confluence) “We selected QA Analytics 4 Life Case Study: Test Automation (API), Functional, Performance, and Security testing Paradigm Quest SoapUI + Ruby Natural language test design (i.e. Gherkin via TDD, BDD) that facilitates ease and quicker automated test scripting Client Case Studies: Today, Test Automation is an integral part of software development and of the software testing process. Agile development has encouraged an increasing shift toward the following: WebDriver IO Proof of Concepts and Pilots JUnit Companies should care about test automation because test automation can: The right process: A methodology that achieves quantifiable results to address challenges, such as maintaining the accuracy of repeatable tasks, expediting the software development life cycle, upgrading technology platforms, and enhancing security. The right technology: A complete set of industry-relevant tools and software licenses to supplement the tools you already have in-house. The right people: Projects led by a team of professionals who have worked with QA teams, business analysts, and developers. The right tools: QA Consultants’ QA professionals have managed automation projects using a wide range of automation technologies. We’ve used Micro Focus/HP UFT, Selenium, Ranorex, Sauce Labs, and Perfecto Mobile, etc. We are a Test Automation Leader QA Consultants is at the forefront of test automation engineering techniques, technologies, and methodologies with our test automation services. We partner with clients across various industries to drive their automation innovation and QA optimization. Our expertise spans all test automation platforms and we have a vast knowledge base of best practices which we leverage for our clients. Companies should care about test automation because test automation can: Reduce testing efforts Deliver projects faster Decrease budgets As a result, we develop and implement the test automation solution that is most appropriate, given your goals, timelines, and budget. Our test automation engineering solution components: The right process: A methodology that achieves quantifiable results to address challenges, such as maintaining the accuracy of repeatable tasks, expediting the software development life cycle, upgrading technology platforms, and enhancing security. The right technology: A complete set of industry-relevant tools and software licenses to supplement the tools you already have in-house. The right people: Projects led by a team of professionals who have worked with QA teams, business analysts, and developers. The right tools: QA Consultants’ QA professionals have managed automation projects using a wide range of automation technologies. We’ve used Micro Focus/HP UFT, Selenium, Ranorex, Sauce Labs, and Perfecto Mobile, etc. The video below shows exactly what QA Consultants can do when it comes to solving difficult problems. The client was convinced their project was un-automatable, however, with our expert knowledge we were able to provide the solution they needed. Click the video below and find out how QA Consultants automated a 14 yearlong automation problem. What happens when test automation goes wrong? Knight Capital, a trading firm in New Jersey City, lost $10 million dollars a minute in 2012 largely in part because they didn’t test their automated trading software. Let that sink in. By the time someone caught the error, the company had lost $440 million, which is more than the company’s revenue of $289 million (in the second quarter). Though this example is an anomaly in terms of extravagant losses, it’s a painful one to realize. This could have easily been avoided if the software development process had included a quality assurance test automation expert that evaluated the software testing approach. The testing process in itself will save money, headaches, and reputation loss; it’s worth the investment. Test Automation Today Today, Test Automation is an integral part of software development and of the software testing process. Agile development has encouraged an increasing shift toward the following: Regular and rapid regression testing The earlier automation of manual testing artefacts (Shift-Left) The utilization of continuous testing (CI/CD)The automation of both unit testing and API testing Natural language test design (i.e. Gherkin via TDD, BDD) that facilitates ease and quicker automated test scripting The reduction in manual testing time and effort for regression testing The usage of open source automation solutions as viable alternatives to commercial tools The different types of test automation comprise GUI test automation, API test automation, and by extension, performance testing. Automated testers and how they apply test automation can fall into either of two categories, that being technical and non-technical. The technical stream indicates that the QA Testers have a development background. Meaning they can get into creating test frameworks and essentially the guts of the test automation. When doing so they may be working in languages such as Java, C++, etc. The non-technical stream denotes that the QA Testers are more manual based testers. As such, they are capable to interface with test automation via certain front ends that have been provided to them. These front ends include a keyword, gherkin, etc. There are two types of popular test automation tools in the market place, those being open source and commercial. The open-source tools revolve around selenium and different languages that can be used with selenium. Languages such as java, javascript, c-sharp, C++, python, groovy, and others. Katalon is a tool based on Selenium and is the natural evolution of open source tools. Commercial tools revolve around Micro Focus, Tricentis, Parasoft, IBM Rational, and Worksoft Certify. A Sample of our Test Automation Clients: QA Consultants is recognized for our broad and expansive test automation capabilities, architecture, building, and maintaining test automation solutions. In turn, we support multi-platform, multi-device, and multi-language/OS forms. QA Consultants applies high levels of sophisticated test automation, utilizing risk-based methodologies, and builds for our clients. We use comprehensive testing modules and libraries for improved productivity including speed to execution. Our model delivers on the promise of a significantly higher quality of testing time to value. In the past four years, over 80% of test projects we’ve completed the required automation. As a result, test automation has driven testing costs down and drastically improve the reusability of automation scripts. With this strength comes innovation in automation in our Test Factory™ that dictates best practices and processes. Testing Tools and Secure Infrastructure Requirements QA Consultants provides every project with all the necessary infrastructure, communication, and software testing tools. As such, we’re prepared to fulfil a complete turnkey solution to address the quality assurance testing needs of our clients. Our unique relationship with HP/Micro Focus, as a premier reseller of their entire test suite of products, provides us with the advantage of delivering the exact test tools and skills on demand. Do note that, any required software tools licensing is included in all of our fees. As a Managed Service Provider (MSP) for HP/Micro Focus, QA Consultants can lease licenses to clients for short periods. In so negating the costly acquisition and ongoing maintenance incurred as part of the licensing costs. A sample of our platforms, tools, and technologies include: Commercial Tools Open Source Tools Customizable Frameworks Mobile Device Management & Automation Other Solution Components Micro Focus Selenium Cucumber Mobile Labs Sonar IBM SoapUI + Ruby Robot Framework DeviceAnywhere Jenkins Microsoft JavaScript JUnit Perfecto Mobile Bamboo Tricentis Python Pytes Appium Fakery Worksoft Katalon WebDriver IO ZAPTEST There are different automation tools for different testing purposes. For instance, if there is the need for the QA Testers to perform API testing, tools such as Katalon, SoapUI, or Parasoft Soatest are recommended. If it is necessary to perform GUI testing, then tools such as Katalon, Selenium, and MicroFocus UFT will suffice. If the QA Testers wish to implement SAP testing, then MicroFocus UFT and Worksoft Certify are preferred. For waterfall SDLC projects test automation typically will be applied toward the latter end of the project. This is simply because it requires a stable GUI for the most part. As well, the nature of a waterfall project has a phase to phase process, and only at the testing phase can test automation essentially begin, however even then a stable GUI is required. Although for agile things are slightly different from waterfall. Within agile, the test automation can begin from the start of the phase to phase process. However, even then test automation’s test coverage will be behind. Nonetheless, test automation itself is creating the regressions test set. Our Testing Services QA Consultants provides the following services as part of our services: Comprehensive Solution Delivery Proof of Concepts and Pilots SDLC (Software Development Life Cycle) Tool Optimization Staff Augmentation Training and Knowledge Transfer QA Consultants’ Team and Management  QA Consultants deploys a “Test Automation Solution” approach to execute best practice QA processes. By working in a collaborative team environment we’re able to produce quality and expedient results. The seasoned expertise of QA Consultants’ test teams becomes more significant when training, orientation, and familiarity with the environment becomes a factor. Our responsiveness to our clients’ needs will ensure a quality outcome, deep rigor, and the use of comprehensive test governance. From an efficiency and effectiveness manner, we have the required knowledge and confidence in our ability to execute project deliverables. Clients will benefit from a quick ramp up, agile project delivery, and a high productivity team. QA Consultants is tools agnostic. We provide solutions based on our clients’ needs. QA Consultants can readily customize any solution. From the high-level conceptual design down to the exact toolset that makes sense to deploy. Here’s what we have to say about Test Automation and being tool agnostic.  QA Consultants | Test Talk Episode 2: Test Automation Client Case Studies: BMO Case Study: Test Automation, Functional Testing CHALLENGE & TEST REQUIREMENTS iVinci Health Treatment Case Study: Manual and Automated Testing “QA Consultants provided a Paradigm Quest Case Study #1: Test Automation (Jira/Zephyr Confluence) “We selected QA Analytics 4 Life Case Study: Test Automation (API), Functional, Performance, and Security testing Contact Us Read more about our Services There are different automation tools for different testing purposes. The right technology: A complete set of industry-relevant tools and software licenses to supplement the tools you already have in-house. on demand For instance, if there is the need for the QA Testers to perform API testing, tools such as Katalon, SoapUI, or Parasoft Soatest are recommended. If it is necessary to perform GUI testing, then tools such as Katalon, Selenium, and MicroFocus UFT will suffice. If the QA Testers wish to implement SAP testing, then MicroFocus UFT and Worksoft Certify are preferred. QA Consultants provides the following services as part of our services: Cucumber Reduce testing efforts Deliver projects faster Decrease budgets any required software tools licensing is included in all of our fees. The video below shows exactly what QA Consultants can do when it comes to solving difficult problems. The client was convinced their project was un-automatable, however, with our expert knowledge we were able to provide the solution they needed. Click the video below and find out how QA Consultants automated a 14 yearlong automation problem. The automation of both unit testing and API testing The right process: A methodology that achieves quantifiable results to address challenges, such as maintaining the accuracy of repeatable tasks, expediting the software development life cycle, upgrading technology platforms, and enhancing security. Regular and rapid regression testing For waterfall SDLC projects test automation typically will be applied toward the latter end of the project. This is simply because it requires a stable GUI for the most part. As well, the nature of a waterfall project has a phase to phase process, and only at the testing phase can test automation essentially begin, however even then a stable GUI is required. Customizable Frameworks Microsoft We are a Test Automation Leader Reduce testing efforts Other Solution Components A Sample of our Test Automation Clients: The right technology: Robot Framework Tricentis Case Study: Manual and Automated Testing “QA Consultants provided a The right tools: QA Consultants’ QA professionals have managed automation projects using a wide range of automation technologies. We’ve used Micro Focus/HP UFT, Selenium, Ranorex, Sauce Labs, and Perfecto Mobile, etc. Microsoft JavaScript JUnit Perfecto Mobile Bamboo QA Consultants | Test Talk Episode 2: Test Automation Testing Tools and Secure Infrastructure Requirements Katalon The different types of test automation comprise GUI test automation, API test automation, and by extension, performance testing. Automated testers and how they apply test automation can fall into either of two categories, that being technical and non-technical. The right people: Projects led by a team of professionals who have worked with QA teams, business analysts, and developers. Knight Capital QA Consultants provides every project with all the necessary infrastructure, communication, and software testing tools. As such, we’re prepared to fulfil a complete turnkey solution to address the quality assurance testing needs of our clients. Our unique relationship with HP/Micro Focus, as a premier reseller of their entire test suite of products, provides us with the advantage of delivering the exact test tools and skills on demand. Do note that, any required software tools licensing is included in all of our fees. As a Managed Service Provider (MSP) for HP/Micro Focus, QA Consultants can lease licenses to clients for short periods. In so negating the costly acquisition and ongoing maintenance incurred as part of the licensing costs. Case Study #1: Test Automation (Jira/Zephyr Confluence) “We selected QA Comprehensive Solution Delivery Commercial Tools Open Source Tools Customizable Frameworks Mobile Device Management & Automation Other Solution Components Micro Focus Selenium Cucumber Mobile Labs Sonar IBM SoapUI + Ruby Robot Framework DeviceAnywhere Jenkins Microsoft JavaScript JUnit Perfecto Mobile Bamboo Tricentis Python Pytes Appium Fakery Worksoft Katalon WebDriver IO ZAPTEST IBM SoapUI + Ruby Robot Framework DeviceAnywhere Jenkins Paradigm Quest Case Study #1: Test Automation (Jira/Zephyr Confluence) “We selected QA Bamboo As a result, we develop and implement the test automation solution that is most appropriate, given your goals, timelines, and budget. Perfecto Mobile Test Factory™ Python ZAPTEST",
#     77))

categories_list = ['Test Automation', 'We are a Test Automation Leader',
                   'What happens when test automation goes wrong?']

image = preprocess(Image.open("../../../../tmpImagesFolder/TEST-AUTOMATION.webp")).unsqueeze(0).to(
    device)
text = clip.tokenize(categories_list).to(device)

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# print("Label probs:", probs)

for index in range(len(probs[0])):
    print("{:<26}".format(categories_list[index]) + " : " + "{:.2%}".format(
        probs[0][index]))
