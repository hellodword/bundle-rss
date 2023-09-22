# rss-bundle

将多个 RSS 源聚合到一起进行输出

## 为什么用 Python

本来是用 Go 的，但它的相关核心库功能不足， [自己实现](https://github.com/hellodword/grss) 太繁琐， libxml2 binding 要引入 CGO，C to Go 还没有好方案。

所以还是用 Python 吧，毕竟 [feedvalidator](https://github.com/w3c/feedvalidator/blob/a9b8d2074f3dc9eb93620d3023ce2348eef25798/requirements.txt) 也是 Python，在规范方面肯定能做得更好更方便。

---

## 组件

### rss-bundle

### rss-proxy

- [ ] 输入格式: rss/atom/json
- [ ] 输出格式: 保持原状/rss/atom
- [ ] 修改 RSS channel 的 Elements
    - [ ] title
    - [ ] link
    - [ ] description
- [ ] 匹配 RSS item 的 Elements
    - [ ] title
    - [ ] link
    - [ ] description
- [ ] 编码
- [ ] 无状态（参数全部在 URL 里）
- [ ] 持久化（通过短网址映射到数据库）
- [ ] insecure
- [ ] User-Agent
- [ ] 正文


---

## ReDoS

- https://www.regular-expressions.info/redos.html
- https://se.ifmo.ru/~ad/Documentation/Mastering_RegExp/mastregex2-CHP-4-SECT-3.html

## TODO

- [ ] 可以为每个源设定 tag
- [ ] 可以自定义源的 title
- [ ] 可以为每个源添加备注
- [ ] 可以单独设定每个源的抓取间隔、是否允许 insecure 等等
- [ ] 可以设定每个源是否去除锚点，也可以通过正则表达式来全局排除
- [ ] 可以设定每个源是否以 link 为唯一 ID，全部入库
- [ ] 可以为每个源设定过滤（考虑是否[独立出来做](#rss-proxy)，类似 [siftrss](https://siftrss.com/)）
- [ ] 可以为每个源设定 user-agent 等参数
- [ ] 源的基础类型是单一的链接，但是也可以是一系列 http requests（相当于可以实现脚本化的 RSSHub）
- [ ] 为操作提供 HTTP API
- [ ] 为操作接入 Telegram Bot 等交互方式
- [ ] 能够以 tag 为粒度设定聚合，可以为 tag 单独配置输出
- [ ] 聚合方式可以是主动推送，也可以是被动生成一个新的 rss，或是别的方式
- [ ] 推送可以设定频率，也可以设定时间点统一推送
- [ ] 推送接入 [apprise](https://github.com/caronc/apprise-api)
