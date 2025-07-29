#ifdef GL_ES
precision mediump float;
#else
// #version 120 // Desktop GLSL version, if needed
#endif

uniform vec2 u_resolution;
uniform float u_time;

varying vec2 v_TexCoord; 

vec2 hash( vec2 p ) {
    p = vec2( dot(p,vec2(127.1,311.7)),
              dot(p,vec2(269.5,183.3)) );
    return -1.0 + 2.0*fract(sin(p)*43758.5453123);
}

float noise( vec2 p ) {
    vec2 i = floor( p );
    vec2 f = fract( p );
    vec2 u = f*f*(3.0-2.0*f); 
    return mix( mix( dot( hash( i + vec2(0.0,0.0) ), f - vec2(0.0,0.0) ),
                     dot( hash( i + vec2(1.0,0.0) ), f - vec2(1.0,0.0) ), u.x),
                mix( dot( hash( i + vec2(0.0,1.0) ), f - vec2(0.0,1.0) ),
                     dot( hash( i + vec2(1.0,1.0) ), f - vec2(1.0,1.0) ), u.x), u.y) + 0.5; 
}

// fractal brownian motion
float fbm(vec2 p, int octaves, float persistence, float lacunarity) {
    float total = 0.0;
    float frequency = 1.0;
    float amplitude = 1.0;
    float maxValue = 0.0;  
    for (int i = 0; i < octaves; i++) {
        total += amplitude * noise(p * frequency);
        maxValue += amplitude;
        amplitude *= persistence; 
        frequency *= lacunarity; 
    }
    if (maxValue == 0.0) return 0.0; 
    return total / maxValue;
}

vec2 toPolar(vec2 cartesian) {
    float angle = atan(cartesian.y, cartesian.x);
    float radius = length(cartesian);
    return vec2(angle, radius);
}

vec2 toCartesian(vec2 polar) {
    return vec2(polar.y * cos(polar.x), polar.y * sin(polar.x));
}

vec4 effect(vec4 color, Image image, vec2 texture_coords, vec2 screen_coords) {
    vec2 uv = (screen_coords.xy / u_resolution.xy) * 2.0 - 1.0;
    uv.x *= u_resolution.x / u_resolution.y;

    float general_time = u_time * 0.07; 

    float modulation_noise_scale = 1.5;
    float modulation_value = noise(uv * modulation_noise_scale + vec2(u_time * 0.03, u_time * 0.04));
    modulation_value = modulation_value * 2.0 - 1.0; 


    
    vec2 polar_uv = toPolar(uv);

    float angle_shift_from_radius = polar_uv.y * (3.0 + modulation_value * 1.5); 


    float base_angle_offset = general_time * 0.8;
    float modulated_angle_offset = modulation_value * 0.5; 

    polar_uv.x += angle_shift_from_radius + base_angle_offset + modulated_angle_offset;


    polar_uv.y += sin(polar_uv.x * (5.0 + modulation_value * 2.0) + general_time * 2.0) * 0.05 * (0.5 + modulation_value * 0.5);


    vec2 spiraled_uv = toCartesian(polar_uv);


    float fbm_noise_scale = 0.5; 
    int fbm_octaves = 4;         
    float fbm_persistence = 0.45; 
    float fbm_lacunarity = 2.1; 

    vec2 animated_fbm_uv_offset = vec2(general_time * 0.3, general_time * 0.2);
    float n = fbm(spiraled_uv * fbm_noise_scale + animated_fbm_uv_offset, fbm_octaves, fbm_persistence, fbm_lacunarity);


    vec3 color1 = vec3(0.1, 0.1, 0.1);
    vec3 color2 = vec3(0.2, 0.2, 0.2);

    vec3 final_color = mix(color1, color2, n);


    return vec4(final_color, 1.0);
}

