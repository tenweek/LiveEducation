YUI.add("yuidoc-meta", function(Y) {
   Y.YUIDoc = { meta: {
    "classes": [
        "ChatBoard",
        "ChatBoardForRecord",
        "CodeEditor",
        "FileDisplay",
        "FileDisplayForRecord",
        "HomePage",
        "HomePageHeader",
        "LivePage",
        "LivePicture",
        "LiveRoom",
        "Login",
        "PageFooter",
        "RecordPage",
        "RecordPicture",
        "RecordRoom",
        "Reset",
        "SignUp",
        "TeachingTools",
        "VideoDisplay",
        "WhiteBoard",
        "WhiteBoardForRecord"
    ],
    "modules": [
        "ChatBoard",
        "ChatBoardForRecord",
        "CodeEditor",
        "FileDisplay",
        "FileDisplayForRecord",
        "HomePage",
        "HomePageHeader",
        "LivePage",
        "LivePicture",
        "LiveRoom",
        "Login",
        "PageFooter",
        "RecordPage",
        "RecordPicture",
        "RecordRoom",
        "Reset",
        "SignUp",
        "TeachingTools",
        "VideoDisplay",
        "WhiteBoard",
        "WhiteBoardForRecord"
    ],
    "allModules": [
        {
            "displayName": "ChatBoard",
            "name": "ChatBoard",
            "description": "实现聊天室功能，\n作为子组件插入直播间页面。"
        },
        {
            "displayName": "ChatBoardForRecord",
            "name": "ChatBoardForRecord",
            "description": "实现聊天室的复现，\n作为子组件插入录播间页面。"
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
            "displayName": "FileDisplayForRecord",
            "name": "FileDisplayForRecord",
            "description": "实现教学区ppt等文件播放的复现，\n作为子组件插入录播间页面，\n用户不能进行任何操作。"
        },
        {
            "displayName": "HomePage",
            "name": "HomePage",
            "description": "直播网站的首页，\n包含导航栏、直播列表、录播列表等信息"
        },
        {
            "displayName": "HomePageHeader",
            "name": "HomePageHeader",
            "description": "页面的导航栏部分，\n在首页、直播间、录播间、直播详情页、录播详情页作为子组件插入。\n包含了直播网站的logo、名字等信息，有首页、直播、录播、登录注册等选项，\n点击可进入相关页面。\n用户在登录后可以看到自己的个人信息并且有修改昵称、密码等功能，\n若用户拥有老师权限则可以进行创建房间。"
        },
        {
            "displayName": "LivePage",
            "name": "LivePage",
            "description": "直播详情页，\n包含正在直播的所有房间缩略图及信息。"
        },
        {
            "displayName": "LivePicture",
            "name": "LivePicture",
            "description": "表示正在直播房间的缩略图，\n包含老师上传的封面图片及房间信息（房间名称、老师名称、在线人数），\n作为子组件插入首页或直播详情页。"
        },
        {
            "displayName": "LiveRoom",
            "name": "LiveRoom",
            "description": "直播间页面"
        },
        {
            "displayName": "Login",
            "name": "Login",
            "description": "登录页面"
        },
        {
            "displayName": "PageFooter",
            "name": "PageFooter",
            "description": "直播网站的footer"
        },
        {
            "displayName": "RecordPage",
            "name": "RecordPage",
            "description": "录播详情页，显示所有录播房间的缩略图及房间信息。"
        },
        {
            "displayName": "RecordPicture",
            "name": "RecordPicture",
            "description": "表示录播房间的缩略图，\n包含老师上传的封面图片及房间信息（房间名称、老师名称），\n作为子组件插入首页或录播详情页。"
        },
        {
            "displayName": "RecordRoom",
            "name": "RecordRoom",
            "description": "录播间页面"
        },
        {
            "displayName": "Reset",
            "name": "Reset",
            "description": "重置密码页"
        },
        {
            "displayName": "SignUp",
            "name": "SignUp",
            "description": "注册页面"
        },
        {
            "displayName": "TeachingTools",
            "name": "TeachingTools",
            "description": "教学区组件，包含白板、ppt、代码编辑器，\n作为子组件插入到直播间页面。"
        },
        {
            "displayName": "VideoDisplay",
            "name": "VideoDisplay",
            "description": "视频直播区域"
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