# 安裝以下套件  
```
pip install flask
pip install line-bot-sdk
pip install openai
pip install selenium
pip install chromedriver-binary
pip install transformers
pip install ckip-transformers
```

# meme_gen_gradio.py  
- 直接執行即可，會回傳本地端網址，以及分享用網址  
- 若中止執行，則 2 份網址皆會刪除  

# meme_gen_linebot.py  
1. 在 ngrok 依序執行以下指令
  ```
  ngrok authtoken "你的 authtoken"
  ngrok http 5000
  ```
  執行完會獲得一組網址  
  ```
  https:// ...... .ngrok-free.app
  ```

2. 執行 meme_gen_linebot.py

3. 在 ngrok 網址 尾端加上 "/webhook" ，貼在如下位置  
![Messaging API](https://github.com/raamiiChu/Meme_Generator/assets/87169493/6f69ac71-038b-4a24-8b11-51c88aa38866)
![upload url](https://github.com/raamiiChu/Meme_Generator/assets/87169493/e654d04d-7792-4633-ae84-be460cde03b1)

4. 點擊 "Verify" 出現以下畫面代表成功  
![check is success](https://github.com/raamiiChu/Meme_Generator/assets/87169493/60739db3-d2a0-496b-995b-20b03e9b1865)
