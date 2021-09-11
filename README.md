![mill](http://keydiary-assets.stor.sinaapp.com/mill-logo.png)

Lightest, themable article system, based on `GitHub`.

### How to

#### Create your own blog

* Fork the repo to your account.
* Modify the `config.js` and save the change.
The format is following this 
```javascript
{   
    // Blog title
    title: 'theorangeclock.github.io',
    // Blog description
    description: 'the lightest blog engine base on github issues.'
    github: {                            
      owner: 'theorangeclock',
      repo: 'theorangeclock.github.io'
    }，
    theme: 'basic'
}
```
* Open `https://your_github_name.github.io/mill` you will see your awesome blog.
* If you want add custom domain for your blog , please check 
https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/

#### Change themes

See [wiki](https://github.com/graffie/mill/wiki/Mill-themes)


#### Development

* Install dependencies `npm i `  
* Build the project `npm run build` 
* Open `http://localhost:4000` check the webpage.



### LICENSE 
This software is free to use under MIT license. See the [LICENSE file][] for license text and copyright information.

[LICENSE file]: https://github.com/theorangeclock/mill/blob/master/LICENSE
