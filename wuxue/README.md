# 武學探索筆記

無建置工具、無外部圖檔或字體依賴的多頁靜態網站。文章與個人介紹均有獨立 HTML 網址。

## 結構

- index.html：首頁、核心主題、三篇精選文章、標籤搜尋。
- about.html：關於作者與探索路徑。
- articles/huashan-sword.html：華山劍法示範文章。
- articles/internal-training.html：內家拳初步筆記。
- articles/spear-game-design.html：長槍與遊戲設計初步筆記。
- style.css：全部頁面的共用樣式。

所有插圖皆為內嵌 SVG；字體使用裝置提供的中文字體，因此不同作業系統的字形可能略有差異。
內容為可修改草稿，參考來源尚未填入。文案未冒充已完成的研究。

## 發布

解壓縮後，將此資料夾內的檔案與 articles 資料夾一同放入 GitHub Pages 的發布目錄；勿只上傳首頁。維持原有相對位置即可。
若原本從儲存庫根目錄發布，就放在根目錄；若從 docs 發布，就全部放在 docs。
此範例沒有代為發布，也沒有修改你現有的 GitHub 儲存庫。

## 本機預覽

在本目錄執行 python3 -m http.server 8000，再開啟 http://localhost:8000。
也可直接開啟 index.html。無須 npm 或打包。

## 編輯與新增文章

1. 修改各 HTML 的文字區塊；修改 style.css 即會影響所有頁面。
2. 複製 articles/huashan-sword.html，另存新檔名。
3. 更新 title、description、h1、正文與側欄目錄。每個章節 id 必須唯一，目錄連結要對應。
4. 在首頁替換或加入 article-card，更新文章 href 與 data-tags。
5. 子頁面引用共用樣式用 ../style.css；回首頁用 ../index.html。

標籤支援 index.html?tag=劍術#recent，從文章內頁返回首頁時會自動篩選。
核心主題與卷軸節點連至相關文章或章節，全部使用標準連結；JavaScript 關閉時仍可閱讀與跨頁導航。
手機導覽展開與搜尋過濾需要 JavaScript。
本網站未使用 dialog、客戶端路由、Markdown 即時載入、外部 API 或根目錄絕對路徑。
