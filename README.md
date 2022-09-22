
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
| [add_tag.py](add_tag.py) | 给一个或多个文件添加tag |
| [delete_tag.py](delete_tag.py) | 给一个或多个文件删除tag |
| [list_no_tag_file.py](list_no_tag_file.py) | 显示指定目录下所有未指定tag的文件 |
| [list_tag.py](list_tag.py) | 显示指定目录下所有文件使用到的tag |
| [query_tag.py](query_tag.py) | 在指定目录下查询含有指定tag的文件 |
| [show_tag.py](show_tag.py) | 显示一个或多个文件的tag |
| [tag_utils.py](tag_utils.py) | tag相关的工具类 |


# 应用举例

* 列出当前目录下所有没有 tag 的文件

```sh
list_no_tag_file.py *
```

* 将当前目录下所有没有 tag 的文件都添加名为 "中文" 的 tag:

```sh
list_no_tag_file.py -print0 *  | xargs -0 add_tag.py 中文
```

> 注意：为了让 `list_no_tag_file.py` 和 `add_tag.py` 能够串联起来，前者需要增加 `-print0` 参数，后者前导的 xargs 命令需要指定 `-0` 参数。

> `-print0` 参数的命名，是借鉴了 `find` 命令的做法。

* 将所有以 "千百惠" 为前缀的文件都添加名为 "中文" 的 tag，并且显示相关文件所有的 tag 信息:

```sh
ls -b 千百惠*  | xargs add_tag.py -print0 中文 | xargs -0 show_tag.py
```

* 将所有tag为 “纯音乐” 的文件拷贝到 `/home/absolute_music` 目录:

```sh
query_tag.py -print0 纯音乐 | xargs -0 -I '{}' cp '{}' /home/absolute_music/
```

