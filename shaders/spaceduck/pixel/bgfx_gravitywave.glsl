#version 330

// @description: passes through texture pixels unchanged

in vec2 uv;
uniform float time;

void main(void) {
    vec4 smpl_base = vec4(1.0,0.2,0.0,1.0);
    gl_FragColor = smpl_base;
}

