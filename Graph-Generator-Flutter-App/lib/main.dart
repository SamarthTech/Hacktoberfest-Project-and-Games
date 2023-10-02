import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:math';

void main() => runApp(MyApp());

class CurveData {
  List<double> voltage;
  List<double> current;

  CurveData({required this.voltage, required this.current});
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  List<CurveData> curveDataList = [];
  LineChart? _lineChart;
  int dataCount = 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
      //   title: Text('Flutter Plot Example'),
      // ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: _lineChart ?? Container(),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  for (int i = 0; i < dataCount; i++) ...[
                    _buildCurveInput(i),
                    Divider(),
                  ],
                  ElevatedButton(
                    onPressed: _generateGraph,
                    child: Text('Generate Graph'),
                  ),
                ],
              ),
            ),
          ),
          ElevatedButton(
            onPressed: _addData,
            child: Text('Add Data Set'),
          ),
        ],
      ),
    );
  }

  Widget _buildCurveInput(int curveNumber) {
    String voltageText = curveDataList.isNotEmpty && curveDataList.length > curveNumber
        ? curveDataList[curveNumber].voltage.join(', ')
        : '';
    String currentText = curveDataList.isNotEmpty && curveDataList.length > curveNumber
        ? curveDataList[curveNumber].current.join(', ')
        : '';

    TextEditingController voltageController = TextEditingController(text: voltageText);
    TextEditingController currentController = TextEditingController(text: currentText);

    return Column(
      children: [
        Text('Curve ${curveNumber + 1} Data:'),
        TextFormField(
          controller: voltageController,
          decoration: InputDecoration(labelText: 'Voltage (V)'),
          keyboardType: TextInputType.text,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter voltage values.';
            }
            final values = value.split(',').map((e) => double.tryParse(e.trim()));
            if (values.any((v) => v == null)) {
              return 'Invalid voltage values. Please enter valid numbers.';
            }
            return null;
          },
          onSaved: (value) {
            final values = value!.split(',').map((e) => double.parse(e.trim())).toList();
            if (curveDataList.length <= curveNumber) {
              curveDataList.add(CurveData(voltage: values, current: []));
            } else {
              curveDataList[curveNumber].voltage = values;
            }
          },
        ),
        TextFormField(
          controller: currentController,
          decoration: InputDecoration(labelText: 'Current (A)'),
          keyboardType: TextInputType.text,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter current values.';
            }
            final values = value.split(',').map((e) => double.tryParse(e.trim()));
            if (values.any((v) => v == null)) {
              return 'Invalid current values. Please enter valid numbers.';
            }
            return null;
          },
          onSaved: (value) {
            final values = value!.split(',').map((e) => double.parse(e.trim())).toList();
            if (curveDataList.length <= curveNumber) {
              curveDataList.add(CurveData(voltage: [], current: values));
            } else {
              curveDataList[curveNumber].current = values;
            }
          },
        ),
      ],
    );
  }

  void _generateGraph() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final List<Color> randomColors = List.generate(
        curveDataList.length,
        (index) => Color.fromRGBO(
          Random().nextInt(256),
          Random().nextInt(256),
          Random().nextInt(256),
          1,
        ),
      );

      final List<LineChartBarData> lineBarsData = [];

      for (int i = 0; i < curveDataList.length; i++) {
        final List<FlSpot> spots = curveDataList[i].voltage.asMap().entries.map((entry) {
          if (entry.value.isNaN) {
            return FlSpot(entry.key.toDouble(), 0);
          }
          return FlSpot(entry.key.toDouble(), curveDataList[i].current[entry.key]);
        }).toList();

        lineBarsData.add(
          LineChartBarData(
            spots: spots,
            isCurved: true,
            colors: [randomColors[i]],
            dotData: FlDotData(show: false),
            belowBarData: BarAreaData(show: false),
          ),
        );
      }

      setState(() {
        _lineChart = LineChart(
          LineChartData(
            gridData: FlGridData(show: false),
            titlesData: FlTitlesData(
              leftTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                margin: 12,
                interval: 2, // Customize the interval for y-axis labels
                getTitles: (value) {
                  return value.toStringAsFixed(1); // Format y-axis labels
                },
              ),
              bottomTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                margin: 12,
                interval: 2, // Customize the interval for x-axis labels
                getTitles: (value) {
                  return value.toStringAsFixed(1); // Format x-axis labels
                },
              ),
            ),
            borderData: FlBorderData(
              show: true,
              border: Border.all(
                color: const Color(0xff37434d),
                width: 1,
              ),
            ),
            minX: 0,
            maxX: curveDataList.isEmpty ? 10 : curveDataList[0].voltage.length.toDouble() - 1,
            minY: 0,
            maxY: 12,
            lineBarsData: lineBarsData,
          ),
        );
      });
    }
  }

  void _addData() {
    setState(() {
      dataCount++;
    });
  }
}
