rich_editor_conf={
    'default': {
         'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', '|',
            'fontColor', 'fontBackgroundColor', 'fontSize', 'fontFamily', '|',
            'alignment', 'indent', 'outdent', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'blockQuote', 'link', 'imageUpload', 'insertTable', 'mediaEmbed', '|',
            'code', 'codeBlock', 'htmlEmbed', '|',
            'horizontalLine', 'pageBreak', 'specialCharacters', '|',
            'undo', 'redo'
        ],
        'language': 'en',
        'pasteFromOffice': {
            'preserveBackgroundColors': True  # This preserves background colors from Word/Excel
        },
        'htmlSupport': {
            'allow': [
                {
                    'name': '/.*/',
                    'attributes': True,
                    'classes': True,
                    'styles': True
                }
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', 'toggleImageCaption', 'imageStyle:inline',
                'imageStyle:block', 'imageStyle:side', 'linkImage'
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells',
                'tableProperties', 'tableCellProperties'
            ]
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4'}
            ]
        },
        'fontFamily': {
            'options': [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Times New Roman, Times, serif',
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif',
            ],
            'supportAllValues': True
        },
        'fontSize': {
            'options': [
                'default',
                '10px',
                '12px',
                '14px',
                '16px',
                '18px',
                '20px',
                '24px',
                '28px',
                '32px'
            ]
        }
    },
    'basic': {
        'toolbar': [
            'bold', 'italic', 'underline', '|',
            'bulletedList', 'numberedList', '|',
            'link', 'blockQuote', '|',
            'undo', 'redo'
        ]
    },
    'document': {
        'toolbar': [
            'heading', '|',
            'fontSize', 'fontFamily', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'alignment', '|',
            'bulletedList', 'numberedList', '|',
            'outdent', 'indent', '|',
            'link', 'imageUpload', 'insertTable', 'blockQuote', 'mediaEmbed', '|',
            'pageBreak', '|',
            'undo', 'redo'
        ],
        'height': '800px',
        'width': '100%'
    }
}