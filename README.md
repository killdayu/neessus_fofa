# neessus_fofa

nessus 扫描c段，然后通过fofa来拿到ip到title，从而判断ip属于哪个资产。

但是目前fofa api调用太多会被ban。

1. 从nessus api获取到host
   1. 返回scans
   2. 选择某个scan
   3. 获取到host
   4. 拿出high和medium的host
   5. 放入dict然后丢给fofa api
2. 使用fofa api获取对应host的title
   1. 从dict里面取出host
   2. 判断ip和域名
   3. 调用fofa api，获取到title
   4. title黑名单，输出host