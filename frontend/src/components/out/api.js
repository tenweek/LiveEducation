YUI.add("yuidoc-meta", function(Y) {
   Y.YUIDoc = { meta: {
    "classes": [
        "ChatRoom",
        "CodeEditor",
        "FileDisplay",
        "HomePage",
        "HomePageHeader",
        "WhiteBoard",
        "WhiteBoardForRecord"
    ],
    "modules": [
        "ChatRoom",
        "CodeEditor",
        "FileDisplay",
        "WhiteBoard",
        "WhiteBoardForRecord"
    ],
    "allModules": [
        {
            "displayName": "ChatRoom",
            "name": "ChatRoom",
            "description": "实现聊天室功能，\n作为子组件插入直播间页面。"
        },
        {
            "displayName": "CodeEditor",
            "name": "CodeEditor",
            "description": "实现教学区代码编辑器功能，\n作为子组件插入直播间页面。\n老师端可以选择不同语言输入代码，\n并同步到学生端。\n学生端不能对代码编辑器进行操作，\n只能同步看到老师的操作。"
        },
        {
            "displayName": "FileDisplay",
            "name": "FileDisplay",
            "description": "实现教学区ppt等文件播放功能，\n作为子组件插入直播间页面。\n老师端可以对ppt做上下翻页等操作，\n学生端不能对白板操作，\n只能同步看到老师的操作。"
        },
        {
            "displayName": "WhiteBoard",
            "name": "WhiteBoard",
            "description": "实现教学区白板功能，\n作为子组件插入直播间页面。\n老师端可以对白板进行操作，\n可以选择画笔、直线、几何图形等进行画图，\n有填充、大小选择、橡皮擦、撤销等功能。\n学生端不能对白板操作，\n只能同步看到老师的操作。"
        },
        {
            "displayName": "WhiteBoardForRecord",
            "name": "WhiteBoardForRecord",
            "description": "实现教学区白板的复现，\n作为子组件插入录播间页面，\n用户不能对白板操作。"
        }
    ],
    "elements": []
} };
});