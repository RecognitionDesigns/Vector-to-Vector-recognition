#!/usr/bin/env python3
#
# Code modified from https://github.com/OlafenwaMoses/ImageAI
#
# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# for use with DDL/Anki's Vector Robot: https://www.anki.com/en-us/vector
    
import anki_vector
from anki_vector.util import degrees, Angle
from imageai.Prediction.Custom import CustomImagePrediction
from PIL import Image, ImageStat

robot = anki_vector.Robot('00703d7c')
robot.connect()
robot.behavior.set_lift_height(1)
robot.behavior.set_head_angle(degrees(2.0))

robot.behavior.say_text("Show me the item to identify. 3, 2, 1, SNAPP")
image = robot.camera.capture_single_image()
image.raw_image.save('capture.jpeg', 'JPEG')
robot.behavior.set_lift_height(0)
#robot.conn.release_control()

#object detection code below
prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
#prediction.setModelPath("model_ex-012_acc-1.000000.h5")
prediction.setModelPath("model_ex-008_acc-0.947368.h5")
prediction.setJsonPath("model_class.json")
prediction.loadModel(num_objects=2)

predictions, probabilities = prediction.predictImage(("capture.jpeg"), result_count=1)
for eachPrediction, eachProbability in zip(predictions, probabilities):
    s = (eachPrediction)
    print(s.replace('_', ' ') , " : " , eachProbability)
#    robot.behavior.say_text("That is definitely {}".format(s.replace('_', ' ')))
    
    if (eachProbability >= 90):
        print("That is definitely {}".format(s.replace('_', ' ')))
#        robot.anim.play_animation_trigger('GreetAfterLongTime')
        robot.behavior.say_text("That is definitely {}".format(s.replace('_', ' ')))

    if (eachProbability <= 89) and (eachProbability >= 60):
        print("That looks like {}".format(s.replace('_', ' ')))
        robot.behavior.say_text("That looks like {}".format(s.replace('_', ' ')))

    if (eachProbability <= 60) and (eachProbability >= 30):
        print("I'm not sure but that looks like {}".format(s.replace('_', ' ')))
        robot.behavior.say_text("I'm not sure but that looks like {}".format(s.replace('_', ' ')))

    if (eachProbability <= 29) and (eachProbability >= 0):
        print("Thats tricky, is it {}".format(s.replace('_', ' ')))
#        robot.anim.play_animation_trigger('CubePounceLoseSession')
        robot.behavior.say_text("Thats tricky, is it {}".format(s.replace('_', ' ')))
#        
    robot.disconnect()