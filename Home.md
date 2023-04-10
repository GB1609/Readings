
---
cssclass: dashboard
banner: "![[sasuke_hitachi.jpg]]"
banner_y: 0.2
banner_lock: true
---
# Readings
- Manga 📚
	- [[Manga Library]]
	- [[Missing Manga]]
- Books 📖
	- [[Book Library]]
# Vault Info
- 🗄️ Recent file updates
 `$=dv.list(dv.pages('').sort(f=>f.file.mtime.ts,"desc").limit(10).file.link)`
- 🔖 Tagged:  favorite 
 `$=dv.list(dv.pages('#favorite').sort(f=>f.file.name,"desc").limit(4).file.link)`
- 〽️ Stats
	- File Count: `$=dv.pages().length`
	- Book count: `$=dv.pages('"Readings/Books"').filter(function(el) { return el.file.name !== "Book database"; }).length`
	- Manga count: `$=dv.pages('"Readings/Manga"').length`