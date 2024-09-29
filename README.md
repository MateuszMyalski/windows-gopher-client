# Windows Gopher Client
![](_articles/assets/gopher/Main_Window.JPG)
In the early days of the internet, exchanging content between people was somewhat difficult. File transfer methods were so complicated that only a few knew how to do it using console commands, not to mention sharing entire directories. That’s how the Gopher protocol was born, created by Mark P. McCahill at the University of Minnesota.

The main purpose of this creation was to enable easy file sharing and browsing between users. Page generators were supposed to use only a few text tags (similarly to HTML, but with a much more limited set), and the pages were meant to be lightweight and have a hierarchical structure.

Even though it's now 2019, and problems with limited data transmission or data indexing no longer concern us, a small group of users still uses this protocol. Many of them utilize it to write so-called gBlogs or to aggregate documents found on the web.

## Browsing Content

To dive into the depths of this small corner of the internet and experience the '90s feel, we can use Linux console browsers like Lynx, the Floodgap Proxy web gateway, or my own Windows version of the browser written in Python.

Using a proxy doesn’t allow for a comfortable browsing experience. When searching the web for a client for Windows systems, I didn’t come across any good alternatives. In fact, the only alternative was an add-on for Mozilla Firefox, which I didn’t like. So, taking advantage of some free time, I wrote an application that displays parsed content associated with the Gopher protocol.

The repository provides access to the source files for potential editing. There is also a fully compiled .exe version, which can be run immediately after downloading (without installation) to browse the content offered by the "internet underground." All the functionality of the application is described under the "About" tab. The browser has an integrated Veronica-2 search engine, offered by the Floodgap community. Simply type the desired phrase into the address bar and click the "GO" button. However, keep in mind that this search engine is not as *intelligent* as Google, so your queries should consist of simple words.

Have Fun!
