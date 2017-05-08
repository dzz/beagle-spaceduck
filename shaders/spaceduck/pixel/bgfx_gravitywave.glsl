#version 330

// @description: passes through texture pixels unchanged

in vec2 uv;
uniform float time;

void main(void) {

    vec2 mod_uv = uv * 8;

    mod_uv.y += sin(time*0.01 + cos(uv.x*2));
    mod_uv.x += cos(time*0.02) + time;
    

    mod_uv.x += sin(time*0.0001);
    mod_uv.y += cos(time*0.0003);
    
    float mod1 = cos(mod_uv.y * 0.2 + time * 0.1 ) * mod_uv.y;
    float v1 = sin(cos(mod_uv.x*1) + mod1 + time);
    float v2 = sin ( mod1 * v1 + time  );


    if(v2<0) { v2 = cos(v1*2+time); }
    if(v1>0) { v1 = cos(v2*2+time); }
    float v3  = sin( cos ( 0.01 * ((v1) * (v2+time)) )*2);
    vec4 smpl_base_1 = vec4(v3-v2,v1*v2,v2-v1,1.0)*cos(time*0.2);
    vec4 smpl_base_2 = vec4(v2-v1,v3*v1,v3-v1*v2,1.0)*sin(time*0.5);
    
    vec4 final_color = gl_FragColor = (smpl_base_1 + smpl_base_2 * sin(time)  ) * vec4(1.0,0.0,1.0,1.0)*0.3;
    final_color.a = 0.1;

    gl_FragColor = final_color;
}

