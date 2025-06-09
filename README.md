# Tongji-Together

同济同行:手机私家车拼车软件(微信小程序)

### 🏗️准备步骤

------

- 安装 `pnpm`
- 安装微信开发者工具

## 📱前端

基于 `uniapp-vue3-vite`

- 🔗 参考模版`uni-preset-vue3-vite`  [点这里](https://github.com/gitboyzcf/uni-preset-vue3-vite?tab=readme-ov-file#uniappvitevue3piniaunocss-小程序h5-项目模板)
- 🔗 参考博客 `uniapp-vue3-vite 搭建小程序、H5 项目模板` [点这里](https://juejin.cn/post/7430827768054775817)
- 🔗 组件库 ***京东风格的轻量级移动端组件库*** `nutui-uniapp` [点这里](https://nutui-uniapp.pages.dev/guide/overview.html)

#### ⚙️启动方式

在 `frontend`目录下执行

```shell
pnpm dev:mp-weixin
```

运行方式：打开 微信开发者工具, 导入 `dist/dev/mp-weixin` 运行。



运行前需要检查**服务端**的 `IP`地址(使用 `ifconfig /ipconfig` 查看),并修改文件 `.env` `.env.development` `.env.production`中的这一行.

```
VITE_APP_PUBLIC_BASE = 'http://xxx.xxx.xxx.xxx:3001'
```



📁重要目录说明

- `@/api` 存放与后端交互的各类`api`,如 `API_LOGIN_POST` , `API_REGISTER_POST`
- `@/layouts` 设置页面布局,如界面底部的导航栏 `tabBar`的设置,每个 `page`的展示都会按照 `layout`进行布局
- `@/pages` 手机应用的各个页面,每个页面需要到 `pages.json` 中注册路由
- `@/store` 应用的持久化信息,如登录后的身份凭证 `token`的持久化存储
- `@/static` 存放如图片等静态元素



## 💻后端

使用 `uv` 进行环境管理,并已创建了虚拟环境和依赖

```shell
uv sync
uv run server.py
```

我们也提供了虚拟环境,使用前只需

```shell
 source .venv/bin/activate
 python server.py
```

后端框架 `Flask`数据库使用 `SQLite`并结合 `SQLAlchemy`实现数据表映射