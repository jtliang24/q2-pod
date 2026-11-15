/* M1 Plus: the player hooks whose V2.1 sites take other instructions than V1.32's (tools/m1plus.py PLAYER_PROFILE's
 * probe_stop, forced_eof, exit_hold and cold_clear). patch/peq_player.c includes this in place of its own, after
 * probe_stop, forced_eof_c, exit_hold_c and PRELOAD_LO; their C and addresses are shared. */
#if M1PLUS
/* From 0x47a4d8 by j, the DFF check's store of the stop code: V2.1 then branches to the check's shared epilogue
 * (0x479e64, frame 0xc0) with the flag's store in the delay slot. Neither runs: the epilogue is done here, and
 * probe_stop does the rest as for DSF and ISO. The j's delay slot, stock's lui $v1, is harmless. */
__asm__(".set push\n.set noreorder\n"
        ".globl probe_stop_dff\nprobe_stop_dff:\n"
        "lw $s0, 0x98($sp)\nlw $s1, 0x9c($sp)\nlw $s2, 0xa0($sp)\nlw $s3, 0xa4($sp)\nlw $s4, 0xa8($sp)\n"
        "lw $s5, 0xac($sp)\nlw $s6, 0xb0($sp)\nlw $s7, 0xb4($sp)\nlw $fp, 0xb8($sp)\nlw $ra, 0xbc($sp)\n"
        "b probe_stop\naddiu $sp, $sp, 0xc0\n.set pop\n");

/* From 0x423310 by jal, in place of stock's sw $a0, 0x14($v1) (mpctx's eof): the jal's delay slot has already loaded
 * $v1 with what the code after needs, so mpctx is read again here. $s0 is the position; every register as it was. */
void forced_eof_m1(int pos) {
    char *mp = MPCTX;
    if (mp && forced_eof_c(mp, pos)) AT(mp, 0x14, int) = 1;
}
__asm__(".set push\n.set noreorder\n.set noat\n.globl forced_eof\nforced_eof:\naddiu $sp, $sp, -88\n"
        "sw $ra, 84($sp)\nsw $v0, 16($sp)\nsw $v1, 20($sp)\nsw $a0, 24($sp)\nsw $a2, 28($sp)\nsw $a3, 32($sp)\n"
        "sw $t0, 36($sp)\nsw $t1, 40($sp)\nsw $t2, 44($sp)\nsw $t3, 48($sp)\nsw $t4, 52($sp)\nsw $t5, 56($sp)\n"
        "sw $t6, 60($sp)\nsw $t7, 64($sp)\nsw $t8, 68($sp)\nsw $t9, 72($sp)\nsw $a1, 76($sp)\n"
        "jal forced_eof_m1\nmove $a0, $s0\n"
        "lw $ra, 84($sp)\nlw $v0, 16($sp)\nlw $v1, 20($sp)\nlw $a0, 24($sp)\nlw $a2, 28($sp)\nlw $a3, 32($sp)\n"
        "lw $t0, 36($sp)\nlw $t1, 40($sp)\nlw $t2, 44($sp)\nlw $t3, 48($sp)\nlw $t4, 52($sp)\nlw $t5, 56($sp)\n"
        "lw $t6, 60($sp)\nlw $t7, 64($sp)\nlw $t8, 68($sp)\nlw $t9, 72($sp)\nlw $a1, 76($sp)\n"
        "jr $ra\naddiu $sp, $sp, 88\n.set pop\n");

/* From 0x4226fc by jal, in the main loop's exit send: stock's lui is $a1's here ({player-status\exit}, 0x88836c), and
 * $a0 is kept. Every register as it was, $a1 stock's lui. */
__asm__(".set push\n.set noreorder\n.set noat\n.globl exit_hold\nexit_hold:\naddiu $sp, $sp, -80\n"
        "sw $ra, 76($sp)\nsw $v0, 16($sp)\nsw $v1, 20($sp)\nsw $a0, 24($sp)\nsw $a2, 28($sp)\nsw $a3, 32($sp)\n"
        "sw $t0, 36($sp)\nsw $t1, 40($sp)\nsw $t2, 44($sp)\nsw $t3, 48($sp)\nsw $t4, 52($sp)\nsw $t5, 56($sp)\n"
        "sw $t6, 60($sp)\nsw $t7, 64($sp)\nsw $t8, 68($sp)\njal exit_hold_c\nsw $t9, 72($sp)\n"
        "lw $ra, 76($sp)\nlw $v0, 16($sp)\nlw $v1, 20($sp)\nlw $a0, 24($sp)\nlw $a2, 28($sp)\nlw $a3, 32($sp)\n"
        "lw $t0, 36($sp)\nlw $t1, 40($sp)\nlw $t2, 44($sp)\nlw $t3, 48($sp)\nlw $t4, 52($sp)\nlw $t5, 56($sp)\n"
        "lw $t6, 60($sp)\nlw $t7, 64($sp)\nlw $t8, 68($sp)\nlw $t9, 72($sp)\nlui $a1, 0x89\n"
        "jr $ra\naddiu $sp, $sp, 80\n.set pop\n");

/* From 0x421a20 by jal, in the main loop: stock's sw $zero, 0xdd0($s6), on the cold path and on the EOF read's way back
 * to it (0x422244), $s6 0xb10000 on both. Touches only $t8, $t9, as V1.32's. */
__asm__(".set push\n.set noreorder\n.set noat\n.globl cold_clear\ncold_clear:\n"
        "1:\nll $t8, " PRELOAD_LO "($s6)\naddiu $t8, $t8, -1\nins $t8, $zero, 1, 1\nli $t9, 3\nmovn $t9, $zero, $t8\n"
        "sc $t9, " PRELOAD_LO "($s6)\nbeqz $t9, 1b\nnop\njr $ra\nnop\n.set pop\n");
#endif
