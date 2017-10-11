/**
 * oscP5message by andreas schlegel
 * example shows how to create osc messages.
 * oscP5 website at http://www.sojamo.de/oscP5
 */
 
import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

PFont myFont;

String  country = "country";
String  name = "name";
String  year = "year";
String  data = "data";

void setup() {
  size(800, 800);
  // Create the font
  myFont = createFont("Georgia", 32);
  textFont(myFont);
  frameRate(15);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 9001);
}

void draw() {
  background(0);
  // Draw the letter to the center of the screen
  textSize(18);
  fill(21, 49, 127);
  text(country, 10, 50, 540, 300);
  text(name, 210, 50, 540, 300);
  text(year, 550, 50, 540, 300);
  text(data, 610, 50, 540, 300);
}

void oscEvent(OscMessage osc_m) {
  /* check if theOscMessage has the address pattern we are looking for. */
  if(osc_m.checkAddrPattern("/woman")==true) {
    /* check if the typetag is the right one. */
    if(osc_m.checkTypetag("ssif")) {
      /* parse theOscMessage and extract the values from the osc message arguments. */
      country = osc_m.get(0).stringValue();   
      name = osc_m.get(1).stringValue();
      year = str(osc_m.get(2).intValue());
      data = str(osc_m.get(3).floatValue());
      println(" values: "+name+", "+name+", "+year+", "+data);     
      return;
    }  
  } 
  println("### received an osc message. with address pattern "+osc_m.addrPattern());
}