# coding=UTF-8

##
# Social Computing Tutorial #4:
#
# @brief Simple Text Analytics with NLTK for generating word cloud on facebook.
#
# @author webofthink@snu.ac.kr
#

#– 자신이 좋아하는 페이지를 찾고 feed의 ‘message’를 수집
#– 전수업에 사용된 방법에 따라서 feed의 Word Cloud 작성
#– 가능하면 next를 이용한 pagination을 사용하세요
#– Word Cloud를 이미지로 저장/캡처해서 facebookfanpage.jpg로 제

import requests
import facebook
