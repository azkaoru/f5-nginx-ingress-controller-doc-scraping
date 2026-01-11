# coding: utf-8
__author__ = 'kwatanabe'

import os
import urllib.request
import urllib.parse
import urllib.error

import yaml
#import urllib2
from lxml import html
import json

class HttpClient(object):

     def __init__(self,proxyUrl):
        if proxyUrl == None:
            pass
        else:
            proxy = {'https': proxyUrl}
            # プロキシハンドラを作成
            proxy_handler = urllib.request.ProxyHandler(proxy)
            # オープナーを作成
            opener = urllib.request.build_opener(proxy_handler)
            # グローバルオープナーを設定
            urllib.request.install_opener(opener)

     def get(self,url):
        request = urllib.request.Request(url)
        request.add_header('User-Agent','curl/7.29.0')
        return urllib.request.urlopen(request)

     def get_honyaku_deepl(self,apikey,text,DEEPL_API_URL= "https://api-free.deepl.com/v2/translate",T_LANG="JA"):
        api_params = {
            "auth_key": apikey,
            "text": text,
            "source_lang": "EN",
            "target_lang": T_LANG,
        }
        # URL エンコード
        encoded_data = urllib.parse.urlencode(api_params).encode('utf-8')
        # リクエストの作成
        request = urllib.request.Request(DEEPL_API_URL, data=encoded_data, method='POST')
        # リクエストの送信とレスポンスの取得
        try:
            with urllib.request.urlopen(request) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data)
                # 翻訳結果の表示
                #print("翻訳結果:", result['translations'][0]['text'])
                return result['translations'][0]['text']
        except urllib.error.HTTPError as e:
            print("HTTPエラー:", e.code, e.reason)
            return None
        except urllib.error.URLError as e:
            print("URLエラー:", e.reason)
            return None


class JRNoteParser(object):
    """JRNoteParser class

    """

    def __init__(self,cache):
        self.cache =cache
        self.httpclient= HttpClient(cache.data['setting']['https.proxy'])
        self.deepl_enable = cache.data['setting']['deepl_enable']
        if self.deepl_enable:
            self.deepl_apikey = cache.data['setting']['deepl_apikey']

    def parse(self,APPEND_KEY="_scraping"):
        content = self.httpclient.get(self.cache.data['setting']['scraping_url'])
        data = content.read()
        for item in self.cache.data['jrnote']:
            #print item
            #print "method:" + str(item)+APPEND_KEY
            search_con= self.cache.data[str(item)+APPEND_KEY]
            settings= self.cache.data['setting']
            if search_con ==None:
                raise Exception("yaml parse err: not found:"+str(item)+APPEND_KEY)
            try:
                getattr(self, str(item)+APPEND_KEY)(data,search_con)
            except Exception as e:
                self.default_scraping(data,search_con)
            #self.scrape_jrnote(content,search_con)

    def normalize_text(self,s):
        return (
            s.replace('\u00a0', ' ')
             .replace('\u200b', '')   # ゼロ幅スペース対策
             .strip()
        )

    def default_scraping(self,data,scrape_con,DEF_ITEM="defaultscraping"):
        content = self.httpclient.get(scrape_con['url'])
        data = content.read()
        elem = html.fromstring(data)

        menu_items =elem.xpath('//div//nav//ol//li//a')
        parent_title = ""
        if len(menu_items) !=0:
            parent_title = '('+ menu_items[len(menu_items)-1].text + ") "

        section_elm = elem.xpath(scrape_con['section'])[0]
        # 配下のすべてのテキストを取得
        all_text = section_elm.xpath('.//text()')
        # リストで取得されるため、結合する場合
        major_tilte = parent_title + ' '.join(all_text)
        # 兄弟要素群を取得
        following_siblings = section_elm.xpath('following-sibling::*')
        minor_item = None
        for fs in following_siblings:
            if fs.tag == "h2" : 
                 break

            bodys=fs.xpath('.//text()')
            empty_check = ' '.join(bodys).strip()
            if empty_check != "" : 
                print (major_tilte,",", "NONE," , "NONE,", "\"",  ' '.join(bodys).strip().replace( '\n', '').replace(",", u"、"), "\"")
        
        comp_elms = section_elm.xpath(scrape_con['componet'])
        join_body = ""
        minor_title = "NONE"
        child_title = "NONE"
        for comp_item in comp_elms: 
            if comp_item.tag == "h2": 
                minor_title = comp_item.xpath("./div//a")[0].text
                child_title = "NONE"
            elif comp_item.tag == "h3":
                child_title = comp_item.xpath("./div//a")[0].text
            bodys = comp_item.xpath('./following-sibling::*')
            for body in bodys:
                if body.tag == "h2" or body.tag == "h3": 
                    break
                body_texts = body.xpath('.//text()')
                join_body = ' '.join(body_texts)
                print (major_tilte ,",", minor_title.strip().replace( '\n', '') + ",", child_title.strip().replace( '\n', '') + ",", "\"",  join_body.strip().replace( '\n', '').replace(",", u"、"), "\"")
 
class JRNoteYAMLCache(object):
    """JRNoteYAMLCache for Yaml Configration

    """
    def __init__(self,DEFAULT_TARGET="../jrnote.yml"):
        self.cache = {}
        base = os.path.dirname(os.path.abspath(__file__))
        self.target =os.path.normpath(os.path.join(base, DEFAULT_TARGET))
        self.data = self._load(self.target)

    def _load(self,target):
        f = open(target,"r")
        #data = yaml.load(f)
        data = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        return data


def main():
    JRNoteParser(JRNoteYAMLCache()).parse()

if __name__ == '__main__':
    main()



