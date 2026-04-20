section .text
    global convertir_y_sumar

convertir_y_sumar:
    
    cvttss2si eax, xmm0    ; convierte float a entero (truncando) y lo guarda en eax
    add eax, 1             ; le suma 1
    ret                    ; devuelve el resultado en eax (que es la parte baja de rax)

section .note.GNU-stack noalloc noexec nowrite progbits

