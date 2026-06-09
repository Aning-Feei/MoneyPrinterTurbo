# 餐厅视频样本图片规范

## 1. 样本目录位置

```text
/Users/feei/AI/restaurant-video-ai-samples
```

## 2. 推荐样本目录结构

```text
restaurant-video-ai-samples/
  sample_name/
    01_intro.jpg
    02_interior.jpg
    03_dish_1.jpg
    04_dish_2.jpg
    05_dish_3.jpg
    06_dining.jpg
    07_detail.jpg
    08_extra.jpg
    project.json
```

## 3. 图片命名规则

- 使用两位数字前缀保证顺序。
- 例如：`01_intro.jpg`、`02_interior.jpg`。
- WebUI 上传时按文件名顺序选择。
- 顺序建议：
  - 门头/招牌
  - 店内环境
  - 招牌菜 1
  - 招牌菜 2
  - 招牌菜 3
  - 用餐场景
  - 细节/服务/锅底
  - 额外亮点

## 4. 图片数量建议

- 30 秒：6-10 张
- 40 秒：7-13 张
- 50 秒：8-16 张
- 60 秒：10-20 张

## 5. 目标时长和片段分配示例

- 30 秒 / 8 张：`4,4,3,4,4,3,4,4`
- 30 秒 / 6 张：`5,5,5,5,5,5`
- 40 秒 / 8 张：`5,5,5,5,5,5,5,5`

说明：片段时长均为整数秒，总和等于目标时长。

## 6. 图片质量建议

- 尽量使用清晰图片。
- 同一方向比例更稳定。
- 避免过暗、模糊、强水印。
- 避免重复过多相似图片。
- 菜品和环境都要有，不能只放菜品。

## 7. project.json

- 当前 WebUI 测试主要依赖手动上传图片。
- `project.json` 可作为样本元信息保留。
- 不要把密钥或个人隐私写入 `project.json`。
