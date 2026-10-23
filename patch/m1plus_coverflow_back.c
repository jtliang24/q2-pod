/* M1 Plus: the title-bar back button every payload page gets. patch/coverflow.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
static int back_return(const void *info) {
    (void)info;
    dispatch_key_return();
    return 0; /* not RET_REPEAT: one shot */
}
/* After the click: the Return closes the page, which must not happen inside the button's dispatch. */
static int back_click(void *ctx, void *event) {
    (void)ctx;
    (void)event;
    timer_add(back_return, 0, 0);
    return STOP;
}

/* M1 Plus has no Return key: every page the payload opens or replaces gets V2.1's title-bar back
 * button at its top left, a Return when clicked (the page's keyup closes it or steps back a screen).
 * Shared with peq_ui.c. */
void *back_button(void *parent) {
    void *button = widget_factory_create_widget(widget_factory(), "button", parent, 0, 0, BACK_W, 48);
    widget_use_style(button, STYLE_NAVBAR_RETURN);
    widget_set_prop_str(button, "style:normal:icon", ICON_RETURN);
    widget_set_prop_str(button, "style:over:icon", ICON_RETURN);
    widget_set_prop_str(button, "style:pressed:icon", ICON_RETURN_DOWN);
    widget_on(button, EVT_CLICK, back_click, 0);
    return button;
}
#endif
