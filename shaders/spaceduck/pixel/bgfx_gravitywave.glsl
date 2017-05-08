#version 330

in vec2 uv;
uniform float time;
uniform float player_y;
uniform float player_x;
uniform sampler2D background;
uniform sampler2D gradient;
uniform sampler2D overlay;
uniform sampler2D distortion_buffer;

void main(void) {

    vec2 overlay_uv = uv + player_x;
    vec2 background_uv = uv;

    background_uv += player_y*-0.02;
    overlay_uv.y += sin(time+uv.x);
    float time_modulated = time + sin(time*2);
    float v1_wiggle_mod = sin((uv.y+time_modulated)*2)*0.3;
    float v1 = sin(uv.x+time+v1_wiggle_mod);
    v1=(v1+1)/2;
    float v1_banded = sin(v1*(7*v1)*4);
    v1_banded = (v1_banded+1)/2;

    vec4 distortion_vector = texture(distortion_buffer, uv );
    
    vec2 grad_coords = vec2( v1 + distortion_vector.r, v1_banded+distortion_vector.g );
    vec4 red = texture( gradient, grad_coords*0.8)*vec4(1.0,0.0,0.0,1.0);
    vec4 green = texture( gradient, grad_coords*1.0 )*vec4(0.0,1.0,0.0,1.0);
    vec4 blue = texture( gradient, grad_coords*1.2 )*vec4(0.0,0.0,1.0,1.0);


    background_uv.x += v1;

    
    overlay_uv.x -= distortion_vector.r;
    overlay_uv.y += distortion_vector.g;

    background_uv.x -= distortion_vector.r;
    background_uv.y += distortion_vector.b;

    vec4 composited = texture(background, background_uv) + (red + green + blue * 0.5) * (1.4*texture( overlay, overlay_uv));
    composited.a = 0.8;
    gl_FragColor = composited * composited;
}

