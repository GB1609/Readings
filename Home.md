---
cssclass: dashboard
banner: "![[sasuke_hitachi.jpg]]"
banner_y: 0.2
banner_lock: true
---

# Notes
- Useful Things
	- [[DistributedFileSystem]]
	- [[Git]]
	- [[Markdown]]
- Google Cloud
	- [[MachineLearning]]
	- [[How Prepare GCP Data Engineer Exam]]
	- [[data_engineering_on_GCP.pdf]]
- Databricks
	- [[Introduction]]
- Apache
	- [[HDFS]]
	- [[Hive]]

# Vault Info
- 🗄️ Recent file updates
 `$=dv.list(dv.pages('').sort(f=>f.file.mtime.ts,"desc").limit(10).file.link)`
- 🔖 Tagged:  favorite 
 `$=dv.list(dv.pages('#favorite').sort(f=>f.file.name,"desc").limit(4).file.link)`
- 〽️ Stats
	- File Count: `$=dv.pages().length`
	- Note Count: `$=dv.pages('"MyNotes"').length`