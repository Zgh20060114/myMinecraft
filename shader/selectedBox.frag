#version 330 core
layout(location=0) out vec4 frag_color;
in vec2 out_uv;
in vec3 out_box_color;
uniform sampler2D texture_selected_box;


void main(){
  vec4 texture_color = texture(texture_selected_box,out_uv);
  frag_color.rgb = texture_color.rgb + out_box_color;
  frag_color.a = texture_color.a;
}
