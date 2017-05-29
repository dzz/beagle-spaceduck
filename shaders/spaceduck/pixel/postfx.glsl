#version 330

// @description: passes through texture pixels unchanged

uniform sampler2D texBuffer;
uniform float pain;
uniform float excitement;
in vec2 uv;

void main(void) {

    vec4 smpl_base = texture(texBuffer,uv);
    vec2 mod_uv = (uv-vec2(0.5,0.5))*2.0;
    float luv = length(mod_uv);
    float l = (smpl_base.r + smpl_base.g + smpl_base.g)/3.0;
    vec4 gray = vec4(l,l,l,1.0);
    float window_size = 0.01;
    vec4 excited = texture(texBuffer,uv+vec2(0.0,window_size))+
                    texture(texBuffer,uv+vec2(0.0,-window_size))+
                    texture(texBuffer,uv+vec2(window_size,0.0))+
                    texture(texBuffer,uv+vec2(-window_size,0.0));
    excited = excited * gray * 0.25;

    
    gl_FragColor = smpl_base * (1.0-(pain)) + (gray*pain) + (excited * excitement);
    //gl_FragColor = vec4(0.0,0.0,0.0,0.0);
}

