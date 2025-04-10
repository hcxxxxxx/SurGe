# 代理配置使用指南

本文档介绍如何为论文搜索系统配置代理，以访问 IEEE、ACM、Google Scholar 和 ArXiv 等学术网站。

## 1. 配置代理的必要性

在某些地区或网络环境中，访问学术网站可能会受到限制，使用代理可以解决以下问题：

- Google Scholar 可能会限制频繁的访问或在某些地区无法访问
- IEEE Xplore 和 ACM Digital Library 可能在某些地区加载缓慢
- ArXiv 在高峰时段可能响应较慢

## 2. 支持的代理类型

系统支持以下几种类型的代理：

- HTTP 代理：最常见的代理类型，格式为 `http://host:port`
- HTTPS 代理：加密的 HTTP 代理，格式为 `https://host:port`
- SOCKS5 代理：支持 TCP/UDP 的通用代理，格式为 `socks5://host:port`

## 3. 配置方法

### 3.1 修改 .env 文件

在项目根目录的 `.env` 文件中配置代理设置：

```
# 是否启用代理
USE_PROXY=true

# 通用代理配置
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
SOCKS_PROXY=socks5://127.0.0.1:1080

# 特定网站的代理配置 (如果需要)
SCHOLAR_PROXY=http://127.0.0.1:7890  # Google Scholar通常需要代理
ARXIV_PROXY=http://127.0.0.1:7890
IEEE_PROXY=http://127.0.0.1:7890
ACM_PROXY=http://127.0.0.1:7890

# 备用代理配置 (当主要代理不可用时)
BACKUP_HTTP_PROXY=http://127.0.0.1:8080
BACKUP_HTTPS_PROXY=http://127.0.0.1:8080
BACKUP_SOCKS_PROXY=socks5://127.0.0.1:1081
```

需要根据实际情况修改代理地址和端口。

### 3.2 常见代理软件配置

#### Clash

如果您使用 Clash 作为代理软件，通常默认端口是：
- HTTP/HTTPS: 7890
- SOCKS5: 7891

配置示例：
```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
SOCKS_PROXY=socks5://127.0.0.1:7891
```

#### V2Ray

如果您使用 V2Ray 作为代理软件，通常默认端口是：
- HTTP: 10809
- SOCKS5: 10808

配置示例：
```
HTTP_PROXY=http://127.0.0.1:10809
HTTPS_PROXY=http://127.0.0.1:10809
SOCKS_PROXY=socks5://127.0.0.1:10808
```

#### 其他代理服务

如果您使用其他代理服务（如付费的代理服务或云代理），请按照提供商的说明配置相应的地址和端口。

## 4. 验证代理是否生效

运行程序后，可以通过查看日志来验证代理是否生效。系统会在日志中输出代理状态信息：

```
INFO:SearchEngine:搜索引擎初始化完成，代理状态: True
INFO:SearchEngine:Google Scholar代理设置成功
INFO:SearchEngine:已为ArXiv设置代理: http://127.0.0.1:7890
```

## 5. 常见问题及增强版解决方案

### 5.1 代理连接失败

如果看到以下错误：
```
ERROR:SearchEngine:从IEEE搜索时出错: HTTPSConnectionPool(host='ieeexplore.ieee.org', port=443): Max retries exceeded with url
```

增强版解决方法：
- 检查代理服务是否正常运行
- 尝试更换代理地址或端口
- 在 `.env` 文件中配置备用代理：
  ```
  BACKUP_HTTP_PROXY=http://替代代理地址:端口
  BACKUP_HTTPS_PROXY=http://替代代理地址:端口
  ```
- 考虑使用付费代理或专业学术代理服务
- 如果是在特定时间出现问题，可能是因为目标服务器繁忙，稍后再试

### 5.2 Google Scholar访问限制

Google Scholar 有严格的反爬虫机制。系统已增强了以下功能：
- 自动重试，带有指数退避策略
- 失败时自动切换到备用爬取方法
- 增加随机延迟模拟人类行为
- 动态调整请求头信息

如果仍然遇到问题：
- 更换 IP 地址或使用高质量代理
- 减少搜索频率
- 考虑使用 Tor 网络（在 `search_engine.py` 中可以启用 Tor 选项）
- 使用 scholarly 的 FreeProxy 功能（在代码中已集成，可通过设置启用）

### 5.3 返回 403 错误（拒绝访问）

如果看到：
```
ERROR:SearchEngine:ACM网站请求失败，状态码: 403
```

增强版解决方法：
- 系统会自动尝试以下方案：
  1. 尝试使用更真实的浏览器头信息
  2. 使用备用的爬取方法
  3. 如果配置了，使用备用代理
  4. 最后尝试使用第三方搜索API

- 您也可以配置 Serper API 作为备用（在 `.env` 文件中）：
  ```
  SERPER_API_KEY=您的Serper API密钥
  ```

### 5.4 所有爬取方法都失败

如果系统仍然无法获取数据：
- 系统会尝试使用本地缓存或内置知识库返回部分基础数据
- 检查您的网络和代理设置
- 尝试更换不同的代理服务商
- 对于特别难以访问的网站，可以考虑手动下载一些论文作为种子数据

## 6. 进阶配置

### 6.1 配置爬虫延迟

在 `config.py` 文件中，可以调整爬虫延迟时间：
```python
CRAWLER_DELAY_MIN = 1  # 最小请求延迟（秒）
CRAWLER_DELAY_MAX = 3  # 最大请求延迟（秒）
```

增大这些值可以减少被网站封禁的风险，但会增加搜索时间。

### 6.2 使用第三方搜索API

对于特别难以访问的网站，系统支持使用 Serper API 作为备用：
1. 注册 Serper API (https://serper.dev/) 并获取API密钥
2. 在 `.env` 文件中设置 `SERPER_API_KEY=您的密钥`

### 6.3 同时使用多种代理

您可以为不同的网站配置不同的代理：
```
SCHOLAR_PROXY=socks5://127.0.0.1:1080  # 为Google Scholar使用SOCKS5代理
IEEE_PROXY=http://premium-proxy.com:8080  # 为IEEE使用高质量付费代理
ACM_PROXY=http://127.0.0.1:7890  # 为ACM使用普通代理
```

## 7. 注意事项

- 使用代理时请遵守相关法律法规和网站的使用条款
- 避免频繁、大量的爬取请求，以免影响网站正常运行或被封禁
- 定期检查代理设置是否仍然有效，因为代理服务器可能会变更
- 考虑使用轮换的IP地址池，特别是对于大量的搜索任务 