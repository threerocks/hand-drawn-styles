# 图片托管与维护规则

项目图片统一托管在 [Netlify 项目 gentle-starburst-99bd99](https://app.netlify.com/projects/gentle-starburst-99bd99/overview)。公开基础地址为 `https://gentle-starburst-99bd99.netlify.app/hand-drawn`。展示图、研发图和运行参考图均使用此地址；Git 与默认安装包只保留链接、清单和审计记录。

## 图片清单与缓存

[`assets/image-manifest.json`](../assets/image-manifest.json) 是图片地址、文件大小和 SHA-256 的真源。图片名称沿用目录路径，名称一旦发布就不能覆盖成不同内容。修改图片必须使用新名称，并同步引用。

`scripts/hosted_images.py` 只使用 Python 标准库。运行 `fetch` 会预取全部 5 张运行参考图；加 `--all` 会预取清单中的全部图片。渲染器按需下载参考图，先检查文件大小和 SHA-256，再写入缓存。正式锚点还要通过原有的尺寸与像素校验。

```bash
python3 -B scripts/hosted_images.py fetch
python3 -B scripts/check_skill.py
```

默认缓存为 `~/.cache/hand-drawn/images`；设置 `XDG_CACHE_HOME` 后使用其中的 `hand-drawn/images`。`HAND_DRAWN_IMAGE_CACHE` 可以指定完整缓存目录。缓存路径包含文件 SHA-256，安装目录不存图片。

首次调用需要联网。有效缓存可以离线复用；`HAND_DRAWN_OFFLINE=1` 禁止自动下载。缓存缺失或损坏时，离线调用报错；联网调用重新下载并校验。下载或校验失败时必须停止需要参考图的调用，禁止退回文字版。普通纯文本配方无需下载。

JSON 调用包的每张画风参考图包含 `url`、`sha256` 和缓存文件的绝对 `path`。调用端仍将 `path` 对应的文件作为图像输入，保留原有的 `style-only`、角色顺序和生产流程。

## 新图片的处理顺序

1. 将新图片保存在仓库外或已忽略的 `dist/` 下。使用 `sweety-image-privacy` 检查并清理 EXIF、GPS、来源字段和 macOS 来源扩展属性，保留审计记录。清理失败时停止该图片发布，不得把「已审计」写成「已清理」。
2. 确定公开路径后登记文件。登记只写清单和本地缓存，不会上传，也不代表公开链接可用：

   ```bash
   python3 -B scripts/hosted_images.py register examples/new-style.png /absolute/path/clean-image.png
   ```

3. 从上面的 Netlify 项目下载**当前生产部署的完整 ZIP**。手动部署会替换整个站点，不能只上传新增图片。构建脚本保留 ZIP 内现有文件，并补齐清单中的所有图片：

   ```bash
   python3 -B scripts/hosted_images.py build-site \
     --base-zip /absolute/path/current-production.zip \
     --output dist/netlify-images/hand-drawn-netlify.zip
   ```

4. 在已获授权的项目中上传该完整 ZIP。保持生产站点公开，等 Netlify 显示 Published 后再验证。执行者必须已有本次图片公开上传的授权；本文不授予其他站点或账号的操作权限。
5. 匿名下载新链接并核对大小及 SHA-256。`verify` 始终读取远端，不会拿缓存代替验证；验证失败时停止提交这些引用：

   ```bash
   python3 -B scripts/hosted_images.py verify examples/new-style.png
   ```

6. 将 Markdown 图片与参考图说明改为清单中的 HTTPS 链接。更新清单、审计记录和必要的运行契约，运行单元测试、安装检查及打包检查。只提交文本，不提交图片、下载缓存或部署 ZIP。

完整托管审计使用 `python3 -B scripts/hosted_images.py verify --all`。静态链接检查只验证链接已登记，不代表远端仍可访问。

## 仓库和安装包限制

`.gitignore` 排除 PNG、JPEG、WebP、GIF、SVG 和 AVIF。仓库检查拒绝已跟踪的图片文件；安装包仅按文本文件清单构建，大小上限为 1 MiB。维护者不得用 `git add -f` 绕过限制。

历史隐私记录按原文保留。图片迁移只证明远端字节与登记文件一致，不改变记录中的隐私或视觉验收结论。Git 历史仍包含旧图片；新安装使用 Release ZIP 或 `git clone --depth 1`，不要为减小当前安装体积改写历史。
