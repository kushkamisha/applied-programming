package ex01;

import java.io.IOException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;


public class CalcT {
private static final String FFSTRING1 = "ABCD/*efgh*/IJK//LMN";

private  Item1 result;

private  Item1 result; 
1private  Item1 result; 

public double calcT (double x, double y){
result.setP(y + Math.hypot(x/2, y) + Math.hypot(x/2, y));  return result.getP();
}

public void init (double x, double y){
result.setXY(x,y);  result.setP(calcT(x,y));
}

