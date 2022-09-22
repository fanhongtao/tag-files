
对文件增加标签(tag)，以方便对文件进行管理。

# 缘起

从QQ音乐中下载了不少音乐mp3文件，下载时，采用的是**下载到同一个目录**方式。这就有一个问题：下载下来的文件不好分类管理。

如果手工将文件拷贝到其它目录，则QQ音乐无法正常管理，后期又需要重新下载。

网络上有一些软件，如：[TagSpaces](https://www.tagspaces.org/)，但用起来都不很顺手，所以想着写一个能满足自己需要的。


# 功能说明

借鉴了 TagSpaces 中将 tag 信息存放在一个特殊目录下，并且每个普通文件对应一个 tag 文件的思路。

添加tag时，会在文件所在目录下，创建一个 `.tag` 子目录，然后在该目录下生成一个 `文件名 + .json` 的 tag 文件。

如，给 `/home/music/张学友 - 烦恼歌.mp3` 添加一个 `中文` 的标签的命令为：

```sh
./add_tag.py 中文 '/home/music/张学友 - 烦恼歌.mp3'
```

命令执行完后，会将标签信息保存到 `/home/music/.tag/张学友 - 烦恼歌.mp3.json` 文件中，文件内容为：

```json
{
  "tags": [
    "中文"
  ]
}
```

# 文件说明

| 文件名 | 功能 |
|:--|:--|
| [tag-add.py](tag-add.py) | 给一个或多个文件添加tag |
| [tag-delete.py](tag-delete.py) | 给一个或多个文件删除tag |
| [tag-list-file-without-tag.py](tag-list-file-without-tag.py) | 显示指定目录下所有未指定tag的文件 |
| [tag-list-tag-used-with-file.py](tag-list-tag-used-with-file.py) | 显示指定目录下所有文件使用到的tag |
| [tag-query-file-with-tag.py](tag-query-file-with-tag.py) | 在指定目录下查询含有指定tag的文件 |
| [tag-show.py](tag-show.py) | 显示一个或多个文件的tag |

> 对外提供的命令，都使用 "tag-" 前缀，这样只需要输入前缀，然后按 TAB 键，让系统联想。以便减少记忆命令的操作。


# 应用举例

* 查询当前目录下所有文件共用了那些tag

```sh
tag-list-tag-used-with-file.py *
```

* 列出当前目录下所有没有 tag 的文件

```sh
tag-list-file-without-tag.py *
```

* 将当前目录下所有没有 tag 的文件都添加名为 "中文" 的 tag:

```sh
tag-list-file-without-tag.py -print0 *  | xargs -0 tag-add.py 中文
```

> 注意：为了让 `tag-list-file-without-tag.py` 和 `tag-add.py` 能够串联起来，前者需要增加 `-print0` 参数，后者前导的 xargs 命令需要指定 `-0` 参数。

> `-print0` 参数的命名，是借鉴了 `find` 命令的做法。

* 将所有以 "千百惠" 为前缀的文件都添加名为 "中文" 的 tag，并且显示相关文件所有的 tag 信息:

```sh
ls -b 千百惠*  | xargs tag-add.py -print0 中文 | xargs -0 tag-show.py
```

* 将所有tag为 “纯音乐” 的文件拷贝到 `/home/absolute_music` 目录:

```sh
tag-query-file-with-tag.py -print0 纯音乐 | xargs -0 -I '{}' cp '{}' /home/absolute_music/
```

