#version 330

// @description: passes through texture pixels unchanged

in vec2 uv;
uniform float time;
uniform sampler2D gradient;
uniform sampler2D overlay;

void main(void) {

    vec2 overlay_uv = uv;

    overlay_uv.y += sin(time+uv.x);
    float time_modulated = time + sin(time*2);
    float v1_wiggle_mod = sin((uv.y+time_modulated)*2)*0.3;
    float v1 = sin(uv.x+time+v1_wiggle_mod);
    v1=(v1+1)/2;
    float v1_banded = sin(v1*(7*v1)*4);
    v1_banded = (v1_banded+1)/2;


    vec2 grad_coords = vec2( v1, v1_banded );
    vec4 red = texture( gradient, grad_coords*0.95)*vec4(1.0,0.0,0.0,1.0);
    vec4 green = texture( gradient, grad_coords*1.0 )*vec4(0.0,1.0,0.0,1.0);
    vec4 blue = texture( gradient, grad_coords*1.01 )*vec4(0.0,0.0,1.0,1.0);


    vec4 composited = (red + green + blue * 0.5) * (1.4*texture( overlay, overlay_uv));
    composited.a = 0.4;
    gl_FragColor = composited;
}

