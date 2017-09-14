# -- coding utf-8 --

Created
on
Fri
Aug
18
150940
2017


@author


KODB

네이버
영화
자동
크롤러
모듈

from bs4 import BeautifulSoup
import urllib.request
import re


# 크롤링 함수
def get_text(URL)
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    count = 0
    for item in soup.find_all(td, class_=[point, title])
        text = text + str(item.find_all(text=True))
        count = count + 1
        if count % 2 == 0
            text = text + str('n')
    return text


def get_first_text(URL)
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all(td, class_=title)
        text = text + str(item.find_all(text=True))
    return text


# 영화 제목 크롤링 함수
def get_movie_name(URL)
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all(span, class_=choice_txt)
        text = text + str(item.find_all(text=True))
    text = clean_title_text(text)
    print(text)
    return text


# 끝페이지 체크함수
def check_max_page(movie_number, i)
    cur_URL = 'httpmovie.naver.commoviepointaflist.nhnst=mcode&sword=' + str(
        movie_number) + '&target=after&page=' + str(i)
    compare_URL = 'httpmovie.naver.commoviepointaflist.nhnst=mcode&sword=' + str(
        movie_number) + '&target=after&page=' + str(i + 1)
    cur_text = get_first_text(cur_URL)
    compare_text = get_first_text(compare_URL)
    if cur_text == compare_text
        print(같다)
        return 1  # 같다
    else
        print(다르다)
        return 2  # 다르다


# 영화제목 클리닝
def clean_title_text(text)
    cleaned_text = re.sub('[[']]', '', text)
    return cleaned_text


# 클리닝 함수
def clean_text(text)
    cleaned_text = re.sub('], '$', text)
    cleaned_text = re.sub('[a-zA-Z]', '', cleaned_text)
    cleaned_text = re.sub('[{}[];)`^-_+@#%&=(']',
                                               '', cleaned_text)
    cleaned_text = re.sub(신고,
                          '', cleaned_text)
    cleaned_text = re.sub(,, ,
    '$', cleaned_text)
    cleaned_text = re.sub(,,
    '', cleaned_text)
    cleaned_text = re.sub($ $,
    '$', cleaned_text)
    return cleaned_text


# 메인 함수
def main()
    for movie_number in range(70492, 71200)
        URL = 'httpmovie.naver.commoviepointaflist.nhnst=mcode&sword=' + str(movie_number) + '&target=after&page=1'
        movie_title = get_movie_name(URL)
        movie_title = re.sub('[]', '', movie_title)
        open_output_file = open(movie_title + str(.txt), 'w', encoding = 'UTF8')
        for i in range(1, 501)
            URL = 'httpmovie.naver.commoviepointaflist.nhnst=mcode&sword=' + str(
                movie_number) + '&target=after&page=' + str(i)
            result_text = get_text(URL)
            open_output_file.write(result_text)
            print(movie_title + 현재페이지
            번호 + str(i) + 현재
            영화
            코드번호 + str(movie_number))
            if check_max_page(movie_number, i) == 1
                break;
        open_output_file.close()
        INPUT_FILE_NAME = movie_title + str(.txt)
        OUTPUT_FILE_NAME = movie_title + str(_cleand.txt)
        read_file = open(INPUT_FILE_NAME, 'r', encoding='UTF8')
        write_file = open(OUTPUT_FILE_NAME, 'w', encoding='UTF8')
        text = read_file.read()
        text = clean_text(text)
        write_file.write(text)
        read_file.close()
        write_file.close()


if __name__ == '__main__'
    main()
