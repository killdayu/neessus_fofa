'''nessus api'''

nessus_baseurl = ""
nessus_accessKey = ""
nessus_secretKey = ""
nessus_headers = {"X-ApiKeys" : "accessKey={}; secretKey={}".format(nessus_accessKey, nessus_secretKey)}

'''fofa api'''
fofa_email = ""
fofa_key = ""
fofa_baseurl = "https://g.fofa.info/api/v1/search/all?email={}&key={}&fields=host,title&qbase64=".format(fofa_email, fofa_key)

fofa_result_keywords_blacklist = ['', 'None', '302 Found', '403 Forbidden', '404 Not Found', 'IIS7',
                                  '400 Bad Request', 'Welcome to nginx!', 'Welcome to nginx for Windows!',
                                  'Error 404--Not Found', 'HTTP Status 404 – 未找到', '403 - 禁止访问: 访问被拒绝。'
                                  'Not Found', 'Apache Tomcat/8.5.58', '文档已移动']  #fofa title 黑名单，屏蔽无意义的输出