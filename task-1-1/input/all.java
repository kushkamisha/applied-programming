package ex01;

import java.io.IOException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

/* Comment1Comment1Comment1Comment1Comment1
Comment1Comment1Comment1
*/
public class CalcT {
private static final String FFSTRING1 = "ABCD/*efgh*/IJK//LMN";

private /* Comment2*/ Item1 result;

private /* Comment3*/ Item1 result; // Comment4 

1private /* Comment3*/ Item1 result; // 1 /* abcdef */ Comment5  


public double calcT (double x, double y){
result.setP(y + Math.hypot(x/2, y) + Math.hypot(x/2, y));  //Comment6
return result.getP();
}

public void init (double x, double y){
result.setXY(x,y); /* Comment7*/ result.setP(calcT(x,y));
}

/* Comment8*/