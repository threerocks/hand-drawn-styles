# #19 暖色扁平绘本验证记录

## 目标

复刻 `reference.webp` 的视觉语言,并验证脱离参考图后能否跨主体稳定复现。

判定维度:

- 轮廓:主要靠色块相接,只有极少深藏青细线。
- 比例:成人长颈细肢、小手脚、窄脸或方下巴;宽体型角色允许巨肩胶囊躯干。
- 配色:暖米白、深藏青、雾蓝、珊瑚橙、金橙、暖桃肤色,不引入额外色相。
- 明暗:每个大色块最多一深一浅两块硬边同色阴影,无写实体积。
- 构图:主体位于下部中央,背景约七成留白,脚下仅一抹淡影。

## 轮次

### r1:材质方向

- `candidate-a-clean-flat.png`:色板基本正确,但偏普通商业矢量,母亲动作与附件差距较大。
- `candidate-b-paper-flat.png`:人物叠放、手势、留白最接近附件,作为后续基线。
- `candidate-c-soft-depth.png`:结构接近,但体积阴影偏重。
- `compare/r1-contact-sheet.png`:从左到右为参考图、A、B、C。
- `compare/final-contact-sheet.png`:从左到右为参考图、最终家庭样图、单人泛化、动物泛化。

### r2:比例与图形修正

`r2/family-refined.png` 只修正四项:父亲巨肩与圆弧抬臂、成人窄脸/方下巴、母亲短发几何块、每块最多一深一浅阴影。其余色板和留白保持 r1-B。

### 无参考图泛化

以下三张均未输入 `reference.webp`,只使用最终候选配方:

- `generalization/librarian.png`:单人抱书,验证细长成人与道具色板。
- `generalization/high-five.png`:双人击掌,验证巨肩/细长体型对比与动作弧线。
- `generalization/bear-and-fox.png`:动物共读,验证非人物题材的几何翻译能力。

三项均保留限定色板、极少轮廓线、平涂硬边阴影和暖白大留白,通过入库门槛。

## 入库结果

- 模板:`STYLES.md` #19。
- 协议登记:`PROTOCOL.md`。
- 最终样图:`examples/19-warm-flat-storybook.png`、`examples/19-warm-flat-storybook-librarian.png`、`examples/19-warm-flat-storybook-animals.png`。
- 隐私审计:`privacy-audit.json`。
