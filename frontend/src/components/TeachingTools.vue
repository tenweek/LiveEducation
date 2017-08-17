<template>
    <div id="teaching-tools">
        <Card>
            <Tabs>
                <Tab-pane label="白板" name="WhiteBoard">
                    <white-board :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></white-board>
                </Tab-pane>
                <Tab-pane label="代码编辑器" name="CodeEditor">
                    <code-editor :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></code-editor>
                </Tab-pane>
                <Tab-pane label="课件展示" name="FileDisplay">
                    <file-display :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></file-display>
                </Tab-pane>
           </Tabs>
        </Card>
    </div>
</template>

<script>
import FileDisplay from './FileDisplay'
import WhiteBoard from './WhiteBoard'
import CodeEditor from './CodeEditor'
export default {
    name: 'teaching-tools',
    props: ['roomId', 'teacherName', 'username'],
    components: {
        FileDisplay,
        CodeEditor,
        WhiteBoard
    }
}
</script>