
EMAIL_ENROLL_TEMPLATE = """Здрасти,
<p>Ти беше записан <b>успешно</b> за курса по <a href="{lifebelt}">{course} ({year})</a> и затова ти изпращаме малко линкове и информация.</p>
<br>
<p>Преди всичко - това е твоята парола и не я казвай на никого: <strong>{pwd}</strong></p>
<br>
<p><a href="{headquarters}">Тук</a> можеш да видиш за това кога си присъствал и забележки, които сме писали за теб.</p>
<p> В <a href="http://lubo.elsys-bg.org/c-programming/">сайта на Любо</a> има обща информация за курса и всичко свързано с ТУЕС. </p>
<br>
<p>Няма нужда да отговаряш на това съобщение, то е генерирано автоматично...</p>
<br>
Поздрави!"""


EMAIL_FORGOT_PWD_TEMPLATE = """Здрасти,
<p>Ти поиска да ти бъде сменена паролата, затова ето ти нова: <strong>{password}</strong></p>
<p>Ако все пак си забравил кое ти е потребителското име: <strong>{username}</strong></p>
<br>
Поздрави!"""

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
