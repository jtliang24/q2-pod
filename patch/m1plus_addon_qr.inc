/* M1 Plus: a card app's QR page (File Browser's), upright. patch/addon.c includes this in qr_open,
 * in place of the Q2's code-beside-text layout (docs/m1plus-roadmap.md U4). */
#if M1PLUS
    /* V2.1's back button and the title in the title bar; the code centred under it, the text below
     * the code; the messages centred on the page. V2.1's theme's label styles. */
    back_button(page);
    widget_set_text_utf8(label(page, BACK_W, 14, UI_W - 2 * BACK_W, 20, STYLE_SCRLABEL_WHITE20C, 16, SPOT_GREY), title);
    qp.qr = widget_factory_create_widget(f, "view", page, (UI_W - QR_PX) / 2, 56, QR_PX, QR_PX);
    qp.col = widget_factory_create_widget(f, "view", page, 16, 56 + QR_PX + 12, UI_W - 32, h - 68 - QR_PX);
    widget_set_text_utf8(label(qp.col, 0, 2, UI_W - 32, 22, STYLE_SCRLABEL_WHITE20L, 18, 0xffffffffu),
                         "Scan with your phone's camera");
    widget_set_text_utf8(label(qp.col, 0, 36, 140, 18, STYLE_SCRLABEL_WHITE20L, 14, SPOT_GREY), "or open");
    qp.addr = label(qp.col, 0, 54, UI_W - 32, 22, STYLE_SCRLABEL_WHITE20L, 16, 0xffffffffu);
    widget_set_text_utf8(label(qp.col, 0, 88, 140, 18, STYLE_SCRLABEL_WHITE20L, 14, SPOT_GREY), "PIN");
    qp.pin = label(qp.col, 0, 106, 140, 28, STYLE_SCRLABEL_WHITE20L, 24, 0xffffffffu);
    qp.note = label(qp.col, 0, 146, UI_W - 32, 20, STYLE_SCRLABEL_WHITE20L, 14, SPOT_GREY);
    qp.msg = widget_factory_create_widget(f, "view", page, 0, BACK_W, UI_W, h - BACK_W);
    qp.say = label(qp.msg, CF_EDGE, 140, UI_W - 2 * CF_EDGE, 30, STYLE_SCRLABEL_WHITE20C, 20, 0xffffffffu);
    qp.sub = label(qp.msg, CF_EDGE, 174, UI_W - 2 * CF_EDGE, 24, STYLE_SCRLABEL_WHITE20C, 16, SPOT_GREY);
#endif
