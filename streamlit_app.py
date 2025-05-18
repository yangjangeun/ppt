# ... 기존 코드 ...
# page_count = st.number_input("페이지 수", min_value=1, value=5, step=1)  # 이 줄 삭제 또는 주석처리

# 슬라이드별 미리보기/수정 이후
if st.button("PPT 생성"):
    prs = Presentation()
    for slide_content in edited_slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        # 제목
        title_shape = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(6.5), Inches(1))
        title_frame = title_shape.text_frame
        title_frame.clear()
        p_title = title_frame.add_paragraph()
        p_title.text = slide_content.get('title', '')
        p_title.font.size = Pt(36)
        p_title.font.bold = True
        p_title.alignment = PP_ALIGN.LEFT
        # 내용
        content_shape = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(6.5), Inches(3.5))
        content_frame = content_shape.text_frame
        content_frame.clear()
        for line in slide_content.get('content', '').split('\n'):
            if line.strip():
                for wrapped_line in textwrap.wrap(line.strip(), width=40):
                    p = content_frame.add_paragraph()
                    p.text = wrapped_line
                    p.font.size = Pt(20)
                    p.alignment = PP_ALIGN.LEFT
    ppt_io = io.BytesIO()
    prs.save(ppt_io)
    st.download_button("PPT 다운로드", ppt_io.getvalue(), file_name="output.pptx")
