package SF;

import java.awt.Color;

import javax.swing.JFrame;


public class Main {
	
	//Game frame size
	public static int frameWidth = 905;
	public static int frameHeight = 700;

	public static void main(String[] args) {
		
		JFrame obj = new JFrame();
		GamePlay gamePlay = new GamePlay();
		
		obj.setBounds(350, 50,frameWidth, frameHeight); //size of the frame
		obj.setTitle("Developed by  Santanu Pal");	//Title of the Game frame
		obj.setBackground(Color.DARK_GRAY);
		obj.setResizable(false);	// Is frame Re-sizable or not
		obj.setVisible(true);		//Frame visible 
		obj.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);		//action on close option
		
		obj.add(gamePlay);

	}

}
