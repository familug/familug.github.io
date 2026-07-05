Title: [TIL] Tạo alias trong fish shell với funcsave
Date: 2025-04-29
Category: frontpage
Tags: fish, shell, alias
Slug: til-fish-alias

Fish shell sử dụng cú pháp khác với các shell truyền thống như bash zsh

````
whatis fish
fish (1)             - the friendly interactive shell
````

### Cấu hình 
Fish không đọc cấu hình từ file `.profile` hay `.*rc` mà cấu hình nằm trong thư mục ~/.config/fish

```
$ find ~/.config/fish/
/home/me/.config/fish/
/home/me/.config/fish/conf.d
/home/me/.config/fish/completions
/home/me/.config/fish/fish_variables
/home/me/.config/fish/functions
/home/me/.config/fish/functions/sshaa.fish
/home/me/.config/fish/functions/gtus.fish
/home/me/.config/fish/functions/gco.fish
/home/me/.config/fish/functions/gd.fish
/home/me/.config/fish/functions/gpo.fish
/home/me/.config/fish/config.fish
```

### alias là function
> alias is a simple wrapper for the function builtin, which creates a function wrapping a command. It has similar syntax to POSIX shell alias. For other uses, it is recommended to define a function.

Để tạo 1 alias mới, viết 

```
alias la='ls -la'
```
Để "save" alias này, gõ 

```
funcsave la
```

sẽ tạo ra 1 file la.fish trong .config/fish/functions:

```
$ type la
la is a function with definition
# Defined via `source`
function la --wraps='ls -la' --description 'alias la=ls -la'
  ls -la $argv; 
end
$ cat ~/.config/fish/functions/la.fish 
function la --wraps='ls -la' --description 'alias la=ls -la'
  ls -la $argv; 
end
```
  
### Kết luận

fish không giống bash.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
