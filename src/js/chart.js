import { Chart, RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export class RadarChart {
    constructor(canvas) {
        this.canvas = canvas;
        this.chart = null;
        this.initChart();
    }
    
    initChart() {
        const ctx = this.canvas.getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: [
                    'Belt Rank Score',
                    'Age Factor',
                    'Weight Factor',
                    'Athleticism Factor',
                    'Experience Factor',
                    'Training Factor',
                    'Competition Factor'
                ],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#f0f6fc',
                            font: {
                                family: 'Inter',
                                size: 14,
                                weight: 500
                            },
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(26, 26, 46, 0.95)',
                        titleColor: '#f0f6fc',
                        bodyColor: '#8b949e',
                        borderColor: 'rgba(0, 212, 255, 0.3)',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        callbacks: {
                            title: function(context) {
                                return context[0].label;
                            },
                            label: function(context) {
                                const value = context.parsed.r;
                                return `${context.dataset.label}: ${value.toFixed(3)}`;
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: this.getMaxScale(),
                        ticks: {
                            color: '#656d76',
                            font: {
                                family: 'Inter',
                                size: 12
                            },
                            stepSize: this.getStepSize(),
                            callback: function(value) {
                                return value.toFixed(1);
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)',
                            lineWidth: 1
                        },
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.15)',
                            lineWidth: 1
                        },
                        pointLabels: {
                            color: '#8b949e',
                            font: {
                                family: 'Inter',
                                size: 13,
                                weight: 500
                            }
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 6,
                        hoverRadius: 8,
                        borderWidth: 2
                    },
                    line: {
                        borderWidth: 3,
                        tension: 0.1
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                interaction: {
                    intersect: false,
                    mode: 'point'
                }
            }
        });
    }
    
    getMaxScale() {
        // Better scaling - BRS is the largest value (800), but factors are mostly 0.8-1.4
        return 2.0; // This will show the multiplier factors properly, BRS will be normalized
    }
    
    getStepSize() {
        return 0.5;
    }
    
    updateData(factorResults, practitionerNames) {
        if (!factorResults || factorResults.length === 0) {
            this.chart.data.datasets = [];
            this.chart.update('none');
            return;
        }
        
        const colors = [
            {
                border: 'rgba(0, 212, 255, 1)',
                background: 'rgba(0, 212, 255, 0.2)',
                point: 'rgba(0, 212, 255, 1)'
            },
            {
                border: 'rgba(157, 78, 221, 1)',
                background: 'rgba(157, 78, 221, 0.2)',
                point: 'rgba(157, 78, 221, 1)'
            }
        ];
        
        this.chart.data.datasets = factorResults.map((factors, index) => {
            const color = colors[index] || colors[0];
            const name = practitionerNames[index] || `Practitioner ${String.fromCharCode(65 + index)}`;
            
            return {
                label: name,
                data: [
                    factors.brs / 400, // Normalize BRS to similar scale as other factors (divide by 400 to get ~0.25-2.0 range)
                    factors.af,
                    factors.wf,
                    factors.acf,
                    factors.ref,
                    factors.tff,
                    factors.cef
                ],
                borderColor: color.border,
                backgroundColor: color.background,
                pointBackgroundColor: color.point,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                borderWidth: 3,
                fill: true
            };
        });
        
        // Animate the update
        this.chart.update('active');
        
        // Add pulsing effect for significant differences
        this.addPulseEffect(factorResults);
    }
    
    addPulseEffect(factorResults) {
        if (factorResults.length !== 2) return;
        
        const [factors1, factors2] = factorResults;
        const factorKeys = ['brs', 'af', 'wf', 'acf', 'ref', 'tff', 'cef'];
        
        // Find factors with significant differences
        const significantDifferences = factorKeys.filter(key => {
            const diff = Math.abs(factors1[key] - factors2[key]);
            const avg = (factors1[key] + factors2[key]) / 2;
            return (diff / avg) > 0.15; // 15% difference threshold
        });
        
        if (significantDifferences.length > 0) {
            // Add visual emphasis to the chart container
            this.canvas.parentElement.classList.add('pulse-animation');
            setTimeout(() => {
                this.canvas.parentElement.classList.remove('pulse-animation');
            }, 2000);
        }
    }
    
    highlightFactor(factorIndex) {
        // Highlight a specific factor on the chart
        if (this.chart.data.datasets.length === 0) return;
        
        // Temporarily increase point size for the highlighted factor
        this.chart.data.datasets.forEach(dataset => {
            const originalRadius = [...dataset.pointRadius];
            dataset.pointRadius = originalRadius.map((radius, index) => 
                index === factorIndex ? 10 : radius
            );
        });
        
        this.chart.update('none');
        
        // Reset after 2 seconds
        setTimeout(() => {
            this.chart.data.datasets.forEach(dataset => {
                dataset.pointRadius = 6;
            });
            this.chart.update('none');
        }, 2000);
    }
    
    exportChart() {
        return this.canvas.toDataURL('image/png');
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}