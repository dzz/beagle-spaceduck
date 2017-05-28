#version 330

// @description: passes through texture pixels unchanged

uniform sampler2D texBuffer;
uniform float pain;
uniform float excitement;
in vec2 uv;

void main(void) {

    vec4 smpl_base = texture(texBuffer,uv);
    vec4 gray = vec4( smpl_base.r, smpl_base.r, smpl_base.r, 1.0);
    vec4 excited = smpl_base;

    gray.b*=0.5;
    gray.g*=0.7;
    excited.g*0.5;
    
    gl_FragColor = smpl_base * (1.0-(pain+excitement)) + (gray*pain) + (excited * excitement);
    //gl_FragColor = vec4(0.0,0.0,0.0,0.0);
}

