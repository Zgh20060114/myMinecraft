#version 330 core
layout(location=0) out vec4 frag_color;
in vec2 out_texture_coord;
uniform sampler2D texture_water; 

void main(){
  vec3 texture_color = texture(texture_water,out_texture_coord).rgb;
  float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
  float fog_arg = 1.0-exp2(-0.000005* fog_dist * fog_dist);
  float alpha = mix(0.5,0.0 ,fog_arg );
  frag_color = vec4(texture_color,alpha);
}
