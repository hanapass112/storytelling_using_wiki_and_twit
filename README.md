# 실시간 Wikipedia, Twit 검색을 통한 스토리텔링(영문) <br>
<br>

## 목차<br>
- 개요 <br>
- 프로세스 <br>
- 데이터수집(Wikipedia, Twitter) <br>
- spaCy: AI-based English NLP package <br>
- 스토리라인 구성<br>
- 실행순서 <br>
- Prerequisites <br>
<br>

## 개요<br>
셀럽, 스포츠스타, 기타 유명한 사건/사고들에 대해서 더 상세한 이야기와 최신소식을 알아볼 수는 없을까?<br>
<br>
인터넷에 있는 수많은 이야기들을 실시간으로 검색해서 이야기를 꾸며볼 수는 없을까? <br>
<br>
Wikipedia는 전세계에서 가장 방대한 백과사전으로 없는 게 없다고 해도 과언이 아니다.<br> 
Twitter는 최신정보를 검색하는데 아주 유용한 SNS이다.(특히 Trump에 대한 소식이라면)<br> 
실시간 Wikipedia, Twitter 검색을 통해 주제(Entity)에 따라 연결성 있는 스토리라인 구성하는 것을 연습해 보자<br>
<br>

## 프로세스<br>
1. 데이터수집 (Wikipedia, Twitter python api)<br>
2. 핵심 Entity추출(spaCy) <br>
3. 스토리라인 구성 <br>
4. 스토리텔링 <br>
<br>

## 스토리라인 구성하기 <br>
여기서는 아주 매끄러운 스토리보다 하나의 키워드에 대해 <br>
 - 다양한 스토리를 이야기 들려주고, <br>
 - 중간에 연관 Entity를 찾아 주제를 전환해서 이야기하는 간단한 구조를 만들어본다. <br>
 <br>
 1) 키워드별 Search  <br>
 2) 스토리선택 & Entity analysis  <br>
 3) 연관 Entity search (Wikipedia, Tiwtter)  <br>
 4) 연결된 스토리선택 (2->4번 반복)  <br>
  <br>
  
## 실행순서  <br>
1. config.json 파일에서 "start_keyword" 값 설정 (notepad 편집 가능)  <br>
2. talker실행: python main_talker.py  <br>
 <br>
 
 ## Prerequisites  <br>
 - Spacy  <br>
 - wikipedia, twitter (python package이름)  <br>
 - urllib  <br>
  <br>
  
  ※ Twitter api access token, secret key등은 반드시 개인키를 발급받아 사용하시기 바랍니다.
   <br>
   
   


