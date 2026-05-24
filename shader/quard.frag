#version 330 core
layout(location=0) out vec4 frag_color;
in uvec2 out_texture_coord;

void main(){
  // gl_FragColor = vec4(0, 0, 0, 1)
  frag_color = out_color;
}
